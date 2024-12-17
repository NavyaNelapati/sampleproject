import logging
import requests
from urllib.parse import urljoin
from base64 import b64encode
from typing import Dict
from tests import constants
import json
import os

logger = logging.getLogger(__name__)


class HttpClient:

    def __init__(self, endpoint, base_url=None) -> None:
        self.base_url = base_url or constants.BASE_URL
        self.client = requests.session()
        self.endpoint = endpoint
        self.headers = {"Content-Type": "application/json"}

    def make_request(
        self,
        method: str,
        headers: Dict = {},
        params: Dict = None,
        payload: Dict = None,
        timeout=10,
    ) -> requests.Response:
        """Make a request using the given method and log the request & response details."""
        try:
            api_endpoint = urljoin(self.base_url, self.endpoint)
            headers = {**headers, **self.headers}
            logging.debug(
                f"Sending request to URL: {api_endpoint} with method: \
                {method}, params: {params}, payload: {payload}"
            )
            response = self.client.request(
                method,
                api_endpoint,
                params=params,
                headers=headers,
                json=payload,
                timeout=timeout,
            )
            return response
        except Exception as ex:
            logging.exception(f"Error making api call, error {ex}")
            raise Exception("Error making api call")

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def create_auth_token(self):
        """Create an authentication token."""
        url = f"{self.base_url}/auth"
        payload = {"username": constants.USER, "password": constants.PASSWORD}
        response = self.client.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def create_auth_header(self):
        token = b64encode(
            f"{constants.USER}:{constants.PASSWORD}".encode('utf-8')
        ).decode("ascii")
        return f'{token}'


def get_test_data():
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = constants.TESTDATA_FILE
        with open(f'{dir_path}/{filename}', 'r') as f:
            test_data = json.load(f)
            return test_data
    except Exception as ex:
        logging.error(f"Unable to load test data {ex}")
        raise Exception("Unable to load test data")


def create_client(endpoint):
    client = HttpClient(endpoint)
    client.context = {}
    return client
