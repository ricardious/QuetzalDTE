import re
from datetime import datetime
from utils.date_utils import parse_date, format_date, is_date_in_range
from models.dte import DTE
from models.authorization import AuthorizationSummary
from services.validator import Validator


class DTEService:
    def __init__(self):
        self.validator = Validator()
        self.processed_references = set()
        self.last_batch = []

    def clear_batch(self):
        self.processed_references.clear()
        self.last_batch.clear()

    def process_requests(self, requests):
        summaries = {}

        for req in requests:
            date_str = self._extract_date(req.timestamp)
            req.date = date_str

            if date_str not in summaries:
                summaries[date_str] = AuthorizationSummary(date_str)
            summary = summaries[date_str]
            summary.received += 1

            errs = self._validate(req, date_str)

            if not any(errs.values()):
                code = self._generate_code(date_str, summary.correct + 1)
                req.approval_code = code
                summary.correct += 1
                summary.approvals.append(
                    {
                        "issuer_nit": req.issuer_nit,
                        "reference": req.reference,
                        "approval_code": code,
                    }
                )
            else:
                for k, v in errs.items():
                    if v:
                        summary.errors[k] += 1

        for summary in summaries.values():
            issuers = set(a["issuer_nit"] for a in summary.approvals)
            
            correct_refs = {a["reference"] for a in summary.approvals}  # Referencias de facturas aprobadas
            receivers = set(
                req.receiver_nit for req in requests 
                if req.date == summary.date and req.reference in correct_refs
            )
            summary.unique_issuers = len(issuers)
            summary.unique_receivers = len(receivers)

        self.last_batch = requests
        return {
            "summaries": [s.to_dict() for s in summaries.values()],
            "total_approved": sum(s.correct for s in summaries.values()),
            "dtes": [r.to_dict() for r in requests],
        }

    def _extract_date(self, ts: str) -> str:
        match = re.search(r"\d{1,2}/\d{1,2}/\d{4}", ts)
        if not match:
            raise ValueError(f"Cannot extract date from timestamp '{ts}'")
        dt = datetime.strptime(match.group(0), "%d/%m/%Y")
        return format_date(dt)

    def _validate(self, req: DTE, date_str: str):
        errs = {
            "issuer_nit": False,
            "receiver_nit": False,
            "vat": False,
            "total": False,
            "duplicate_reference": False,
        }
        if not self.validator.validate_nit(req.issuer_nit):
            errs["issuer_nit"] = True
        if not self.validator.validate_nit(req.receiver_nit):
            errs["receiver_nit"] = True

        expected_vat = round(req.amount * 0.12, 2)
        if abs(req.vat - expected_vat) > 0.01:
            errs["vat"] = True

        if abs(req.total - (req.amount + req.vat)) > 0.01:
            errs["total"] = True

        key = f"{date_str}_{req.reference}"
        if key in self.processed_references:
            errs["duplicate_reference"] = True
        else:
            self.processed_references.add(key)

        return errs

    def _generate_code(self, date_str: str, seq: int) -> str:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return dt.strftime("%Y%m%d") + str(seq).zfill(8)

    def get_vat_summary_by_date(self, date_str: str):
        filtered = [r for r in self.last_batch if r.date == date_str]
        vat_per_nit = {}
        for r in filtered:
            vat_per_nit.setdefault(r.issuer_nit, 0.0)
            vat_per_nit[r.issuer_nit] += r.vat
        return {
            "date": date_str,
            "vat_summary": [
                {"issuer_nit": nit, "total_vat": round(v, 2)}
                for nit, v in vat_per_nit.items()
            ],
        }

    def get_summary_by_range(self, start: str, end: str, mode: str):
        total = 0.0
        for r in self.last_batch:
            if is_date_in_range(r.date, start, end):
                total += (r.amount + r.vat) if mode == "total" else r.amount
        return {"start": start, "end": end, "mode": mode, "summary": round(total, 2)}
