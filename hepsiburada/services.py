from urllib.parse import urljoin
from adminpage.models import Hepsiburada
from hepsiburada import api


class BaseService:

    def __init__(self, api: 'api.HepsiburadaApiClient'):
        self._api = api
        self.base_url = "https://mpop-sit.hepsiburada.com/product/api/"


class HepsiburadaProductIntegrationService(BaseService):

    def __init__(self, api: 'api.HepsiburadaApiClient'):
        super(HepsiburadaProductIntegrationService, self).__init__(api)

    def get_categories(self, page):
        endpoint = "categories/get-all-categories"
        url = urljoin(self.base_url, endpoint)

        params = {
            "size": 2000,
            "page": page
        }

        data = self._api.call("GET", url, params=params, headers=None, files=None)
        return data

    def get_category_attributes(self, categoryId):
        endpoint = "categories/{}/attributes".format(categoryId)
        url = urljoin(self.base_url, endpoint)
        params = {
            "categoryId": categoryId
        }
        data = self._api.call("GET", url, params=params, headers=None, files=None)
        return data

    def get_attributes(self, categoryId, attributeId):
        endpoint = "categories/{}/attribute/{}/values".format(categoryId, attributeId)
        url = urljoin(self.base_url, endpoint)
        params = {
            "categoryId": categoryId,
            "attributeId": attributeId
        }
        data = self._api.call("GET", url, params=params, headers=None, files=None)
        return data

    def get_products(self, filter_params=None):
        endpoint = "https://listing-external-sit.hepsiburada.com/Listings/merchantid/{}".format(Hepsiburada.merchantID)
        params = {
            "offset": filter_params.get("offset", 0),
            "limit": filter_params.get("limit", 10),
            "hbSkuList": filter_params.get("hbSkuList", None),
            "merchantSkuList": filter_params.get("merchantSkuList", None),
            "salable-listings": filter_params.get("salable-listings", None),
            "updateStartDate": filter_params.get("updateStartDate", None),
            "updateEndDate": filter_params.get("updateEndDate", None),
        }

        url = urljoin(self.base_url, endpoint)
        data = self._api.call("GET", url, params=params, headers=None, files=None)
        return data

    def create_products(self, files):
        endpoint = "products/import"
        url = urljoin(self.base_url, endpoint)
        hepsiburada = Hepsiburada.objects.all().last()
        headers = {
            "accept": "application/json",
            "content-type": "multipart/form-data",
            "authorization": "Basic " + hepsiburada.token,
        }

        data = self._api.call("POST", url, headers=headers, files=files)
        return data

    def update_products(self, items):
        url = "https://mpop-sit.hepsiburada.com/ticket-api/api/integrator/import"
        params = {
            "items": items
        }
        data = self._api.call("PUT", url, params=params, headers=None, files=None)
        return data

    def update_stock(self, items):

        url = "https://listing-external-sit.hepsiburada.com/Listings/merchantid/{}/stock-uploads".format(
            Hepsiburada.merchantID)
        payload = [items]

        result = self._api.call("POST", url, data=payload, headers=None, files=None)
        return result

    def update_price(self, items):

        url = "https://listing-external-sit.hepsiburada.com/Listings/merchantid/{}/price-uploads".format(
            Hepsiburada.merchantID)

        payload = [items]

        result = self._api.call("POST", url, data=payload, headers=None, files=None)
        return result

    def get_batch_requests(self, batch_request_id, supplier_id=None):
        if supplier_id:
            endpoint = "suppliers/{supplier_id}/products/batch-requests/{batch_request_id}".format(
                supplier_id=supplier_id,
                batch_request_id=batch_request_id
            )
        else:
            endpoint = "suppliers/{supplier_id}/products/batch-requests/{batch_request_id}".format(
                supplier_id=self._api.supplier_id,
                batch_request_id=batch_request_id
            )
        url = urljoin(self.base_url, endpoint)
        data = self._api.call("GET", url, params=None, headers=None, files=None)
        return data

    def deleted_product(self, sku, merchantSku):

        url = "https://listing-external-sit.hepsiburada.com/Listings/merchantid/{}/sku/{}/merchantsku/{}".format(Hepsiburada.merchantID, sku, merchantSku)

        data = self._api.call("DELETE", url, headers=None)
        return data


class OrderIntegrationService(BaseService):

    def __init__(self, api):
        super(OrderIntegrationService, self).__init__(api)

    def get_shipment_packages(self, filter_params, supplier_id=None):
        if supplier_id:
            endpoint = "suppliers/{}/orders".format(supplier_id)
        else:
            endpoint = "suppliers/{}/orders".format(self._api.supplier_id)
        if not filter_params:
            filter_params = {}
        params = {
            "startDate": filter_params.get("startDate", None),
            "endDate": filter_params.get("endDate", None),
            "page": filter_params.get("page", None),
            "size": filter_params.get("size", None),
            "orderNumber": filter_params.get("orderNumber", None),
            "status": filter_params.get("status", None),
            "orderByField": filter_params.get("orderByField", None),
            "orderByDirection": filter_params.get("orderByDirection", None),
            "shipmentPackageIds": filter_params.get("shipmentPackageIds", None)
        }
        url = urljoin(self.base_url, endpoint)
        data = self._api.call("GET", url, params=params, headers=None, files=None)
        return data

    def get_awaiting_shipment_packages(self):
        pass

    def update_tracking_number(self, shipment_package_id, tracking_number, supplier_id=None):
        if supplier_id:
            endpoint = "suppliers/{supplier_id}/{shipment_package_id}/update-tracking-number".format(
                supplier_id=supplier_id,
                shipment_package_id=shipment_package_id
            )
        else:
            endpoint = "suppliers/{supplier_id}/{shipment_package_id}/update-tracking-number".format(
                supplier_id=self._api.supplier_id,
                shipment_package_id=shipment_package_id
            )
        url = urljoin(self.base_url, endpoint)
        params = {
            "trackingNumber": tracking_number
        }
        data = self._api.call("PUT", url, params=params, headers=None, files=None)
        return data

    def update_shipment_package(self, shipment_package_id, status, lines=None, params=None, supplier_id=None):
        if supplier_id:
            endpoint = "suppliers/{supplier_id}/shipment-packages/{shipment_package_id}".format(
                supplier_id=supplier_id,
                shipment_package_id=shipment_package_id
            )
        else:
            endpoint = "suppliers/{supplier_id}/shipment-packages/{shipment_package_id}".format(
                supplier_id=self._api.supplier_id,
                shipment_package_id=shipment_package_id
            )
        url = urljoin(self.base_url, endpoint)
        params = {
            "status": status
        }
        if lines:
            params["lines"] = lines
        if params:
            params["params"] = params
        data = self._api.call("PUT", url, params=params, headers=None, files=None)
        return data

    def update_package_as_unsupplied(self):
        pass

    def send_invoice_link(self):
        pass

    def split_multi_package_by_quantity(self):
        pass

    def split_shipment_package(self):
        pass

    def split_multi_shipment_package(self):
        pass

    def split_shipment_package_by_quantity(self):
        pass

    def update_box_info(self):
        pass

    def process_alternative_delivery(self):
        pass

    def change_cargo_provider(self):
        pass


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
