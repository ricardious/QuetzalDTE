import os
import xml.etree.ElementTree as ET
from models.dte import DTE
from config import Config


class XMLService:
    def __init__(self):
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        self.path = Config.AUTHORIZATIONS_FILE
        if not os.path.exists(self.path):
            self._init_file()

    def _init_file(self):
        root = ET.Element("AuthorizationsList")
        ET.ElementTree(root).write(self.path, encoding="utf-8", xml_declaration=True)

    def read_requests(self, xml_file) -> list[DTE]:
        requests = []
        try:
            tree = ET.parse(xml_file)
            for elem in tree.getroot().findall(".//DTE"):
                try:
                    dto = DTE(
                        timestamp=elem.findtext("TIEMPO"),
                        reference=elem.findtext("REFERENCIA"),
                        issuer_nit=elem.findtext("NIT_EMISOR"),
                        receiver_nit=elem.findtext("NIT_RECEPTOR"),
                        amount=float(elem.findtext("VALOR") or 0),
                        vat=float(elem.findtext("IVA") or 0),
                        total=float(elem.findtext("TOTAL") or 0),
                    )
                    requests.append(dto)
                except Exception:
                    continue
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {e}")
        return requests

    def save_authorizations(self, result):
        tree = ET.parse(self.path)
        root = tree.getroot()
        for summary in result["summaries"]:
            auth_el = ET.SubElement(root, "Authorization")
            ET.SubElement(auth_el, "DATE").text = summary["date"]
            ET.SubElement(auth_el, "RECEIVED").text = str(summary["received"])
            errs_el = ET.SubElement(auth_el, "ERRORS")
            for k, v in summary["errors"].items():
                ET.SubElement(errs_el, k.upper()).text = str(v)
            ET.SubElement(auth_el, "CORRECT").text = str(summary["correct"])
            ET.SubElement(auth_el, "UNIQUE_ISSUERS").text = str(
                summary["unique_issuers"]
            )
            ET.SubElement(auth_el, "UNIQUE_RECEIVERS").text = str(
                summary["unique_receivers"]
            )
        tree.write(self.path, encoding="utf-8", xml_declaration=True)

    def read_authorizations(self):
        tree = ET.parse(self.path)
        out = []
        for elem in tree.getroot().findall("Authorization"):
            out.append({child.tag.lower(): child.text for child in elem})
        return {"authorizations": out}

    def reset_authorizations(self):
        self._init_file()
