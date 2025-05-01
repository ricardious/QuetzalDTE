class DTE:
    def __init__(
        self,
        timestamp=None,
        reference=None,
        issuer_nit=None,
        receiver_nit=None,
        amount=0.0,
        vat=0.0,
        total=0.0,
    ):
        self.timestamp = timestamp
        self.reference = reference
        self.issuer_nit = issuer_nit
        self.receiver_nit = receiver_nit
        self.amount = amount
        self.vat = vat
        self.total = total
        self.date = None
        self.approval_code = None

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "reference": self.reference,
            "issuer_nit": self.issuer_nit,
            "receiver_nit": self.receiver_nit,
            "amount": self.amount,
            "vat": self.vat,
            "total": self.total,
            "date": self.date,
            "approval_code": self.approval_code,
        }
