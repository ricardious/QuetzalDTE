from services.dte_service import DTEService
from services.xml_service import XMLService


class DTEController:
    def __init__(self):
        self.dte_service = DTEService()
        self.xml_service = XMLService()

    def process_requests(self, xml_file):
        requests = self.xml_service.read_requests(xml_file)

        result = self.dte_service.process_requests(requests)

        self.xml_service.save_authorizations(result)

        return {
            "requests_processed": len(requests),
            "authorizations_generated": result["total_approved"],
        }

    def get_authorizations(self):
        return self.xml_service.read_authorizations()

    def get_vat_summary_by_date(self, date_str):
        return self.dte_service.get_vat_summary_by_date(date_str)

    def get_summary_by_range(self, start_str, end_str, mode):
        return self.dte_service.get_summary_by_range(start_str, end_str, mode)

    def reset(self):
        self.dte_service.clear_batch()
        self.xml_service.reset_authorizations()
