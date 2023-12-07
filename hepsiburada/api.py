from json import dumps
import requests
from hepsiburada.exceptions import HepsiburadaAPIError

def json_encode(data, ensure_ascii=False, encoding="utf-8"):
    return dumps(data, ensure_ascii=ensure_ascii).encode('utf-8')

class HepsiburadaApiClient:

    def __init__(self, username, password, mercant_id, integrator_name="SelfIntegration", is_test=False):
        self.username = username
        self.password = password
        self.mercant_id = mercant_id
        self.integrator_name = integrator_name
        self.is_test = is_test
        self._session = HepsiburadaSession(username, password)

    def call(self, method, url, params=None, headers=None, files=None):
        if not params:
            params = {}
        if not headers:
            headers = {}
        if not files:
            files = {}

        # set headers
        user_agent = "{} - {}".format(self.mercant_id, self.integrator_name)
        headers.update({
            "Content-Type": "application/json;charset=utf-8",
        })
        # call request
        if method in ('GET', 'DELETE'):
            response = self._session.requests.request(
                method,
                url,
                params=params,
                headers=headers,
                files=files,
                timeout=self._session.timeout
            )

        else:
            # Encode params
            params = json_encode(params)
            response = self._session.requests.request(
                method,
                url,
                data=params,
                headers=headers,
                files=files,
                timeout=self._session.timeout
            )

        if response.ok:
            return response.json()
        else:
            raise HepsiburadaAPIError("Call not successfull", response)


class HepsiburadaSession:

    def __init__(self, username, password, timeout=None, http_adapter=None):
        self.username = username,
        self.password = password
        self.timeout = None
        self.http_adapter = http_adapter
        self.requests = requests.Session()
        self.requests.auth = (username, password)
        if http_adapter:
            self.requests.mount("https://", http_adapter)