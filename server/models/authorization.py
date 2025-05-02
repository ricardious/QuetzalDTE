class AuthorizationSummary:
    def __init__(self, date):
        self.date = date
        self.received = 0
        self.errors = {
            "issuer_nit": 0,
            "receiver_nit": 0,
            "vat": 0,
            "total": 0,
            "duplicate_reference": 0,
        }
        self.correct = 0
        self.unique_issuers = 0
        self.unique_receivers = 0
        self.approvals = []

    def to_dict(self):
        return {
            "date": self.date,
            "received": self.received,
            "errors": self.errors,
            "correct": self.correct,
            "unique_issuers": self.unique_issuers,
            "unique_receivers": self.unique_receivers,
            "approvals": self.approvals,
            "total_approved": len(self.approvals),
        }
