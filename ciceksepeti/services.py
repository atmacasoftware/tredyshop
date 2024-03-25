from urllib.parse import urljoin
from ciceksepeti.models import Ciceksepeti
from ciceksepeti import api


class BaseService:

    def __init__(self, api: 'api.CiceksepetiApiClient'):
        self._api = api
        if self._api.is_test:
            self.base_url = "https://sandbox-apis.ciceksepeti.com/api/"
        else:
            self.base_url = "https://apis.ciceksepeti.com/api/"

class ProductIntegrationService(BaseService):

    def __init__(self, api: 'api.CiceksepetiApiClient'):
        super(ProductIntegrationService, self).__init__(api)

    def get_categories(self):
        endpoint = "v1/Categories"
        url = urljoin(self.base_url, endpoint)
        data = self._api.call("GET", url, params=None, headers=None, files=None)
        return data

    def get_category_attributes(self, category_id):
        endpoint = "v1/Categories/{}/attributes".format(category_id)
        url = urljoin(self.base_url, endpoint)
        params = {
            "category_id": category_id
        }
        data = self._api.call("GET", url, params=params, headers=None, files=None)
        return data

    def get_products(self, filter_params=None):

        endpoint = "v1/Products"
        if not filter_params:
            filter_params = {}
        params = {
            "ProductStatus": filter_params.get("ProductStatus", None),
            "PageSize": filter_params.get("PageSize", None),
            "Page": filter_params.get("Page", None),
            "SortMethod": filter_params.get("SortMethod", None),
            "StockCode": filter_params.get("StockCode", None),
            "variantName": filter_params.get("variantName", None),
        }

        url = urljoin(self.base_url, endpoint)
        data = self._api.call("GET", url, params=params, headers=None, files=None)
        return data

    def create_products(self, items):
        endpoint = "v1/Products"
        url = urljoin(self.base_url, endpoint)
        data = self._api.call("POST", url, params=items, headers=None, files=None)
        return data

    def update_stok_price(self, items):
        endpoint = "v1/Products/price-and-stock"
        url = urljoin(self.base_url, endpoint)
        data = self._api.call("PUT", url, params=items, headers=None, files=None)
        return data


    def get_batch_requests(self, batch_request_id,):
        endpoint = "v1/Products/batch-status/{batchId}".format(
            batchId=batch_request_id
        )
        url = urljoin(self.base_url, endpoint)
        data = self._api.call("GET", url, params=None, headers=None, files=None)
        return data


class CommonLabelIntegrationService(BaseService):

    def __init__(self, api):
        super(CommonLabelIntegrationService, self).__init__(api)

    def create_common_label(self):
        pass

    def get_common_label(self):
        pass

    def get_common_label_v2(self):
        pass


class ReturnedOrdersIntegrationService(BaseService):

    def __init__(self, api):
        super(ReturnedOrdersIntegrationService, self).__init__(api)

    def get_shipment_packages(self):
        pass

    def create_claim(self):
        pass

    def approve_claim_line_items(self):
        pass

    def create_claim_issue(self):
        pass

    def get_claim_issue_reasons(self):
        pass

    def get_claim_audits(self):
        pass


class AccountingAndFinanceIntegrationService(BaseService):

    def __init__(self, api):
        super(AccountingAndFinanceIntegrationService, self).__init__(api)

    def filter_with_date_validation_constraint(self):
        pass

    def get_settlements(self):
        pass

    def get_other_financials(self):
        pass


class QuestionAndAnswerIntegrationService(BaseService):

    def __init__(self, api):
        super(QuestionAndAnswerIntegrationService, self).__init__(api)

    def get_question_filters(self):
        pass

    def get_question_filter_by_id(self):
        pass

    def create_answer(self):
        pass
