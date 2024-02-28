import json

import requests
from trendyol_sdk.utils import json_encode
from ciceksepeti.exceptions import CiceksepetiAPIError


class CiceksepetiApiClient:

    def __init__(self, api_key, supplier_id, integrator_name="SelfIntegration", is_test=False):
        self.api_key = api_key
        self.supplier_id = supplier_id
        self.integrator_name = integrator_name
        self.is_test = is_test

    def call(self, method, url, params=None, headers=None, files=None):
        if not params:
            params = {}
        if not headers:
            headers = {}
        if not files:
            files = {}
        # set headers
        headers.update({
            "x-api-key": f"{self.api_key}",
            "Content-Type": "application/json;charset=utf-8",
        })
        # call request
        if method in ('GET', 'DELETE'):
            response = requests.request(
                method,
                url,
                params=params,
                headers=headers,
                files=files,
            )

        else:
            params = json_encode(params)

            response = requests.request(
                method,
                url,
                data=params,
                headers=headers,
                files=files,
            )

        if response.ok:
            return response.json()
        else:
            raise CiceksepetiAPIError("Call not successfull", response)

