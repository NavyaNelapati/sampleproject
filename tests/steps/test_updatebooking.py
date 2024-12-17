from pytest_bdd import scenarios, given, when, then, parsers
from tests.utils import HttpClient

import logging

logger = logging.getLogger(__name__)
# Load all scenarios from the feature file
scenarios("../features/updateBooking.feature")


@given(
    parsers.parse('user has access to endpoint "{endpoint}"'),
    target_fixture="apiclient",
)
def create_client(endpoint):
    client = HttpClient(endpoint)
    client.context = {}
    return client


@given('user creates a auth token with credentials')
def create_auth_tokens(apiclient, context):
    token = apiclient.create_auth_token()
    context["auth_token"] = token['token']


@when(
    parsers.parse(
        'user send a "{method}" to "{bookingidkey}" using data "{recordKey}" from test data'
    )
)
def update_booking_record(
    context, apiclient, method, bookingidkey, recordKey, testdata
):

    headers = {"Cookie": f"token={context['auth_token']}"}
    booking_data = testdata[recordKey]
    bookingid = testdata[bookingidkey]
    logger.info(f"invoking update booking scenario for given booking id {bookingid}")
    apiclient.set_endpoint(f"/booking/{bookingid}")
    response = apiclient.make_request(
        method=method, headers=headers, payload=booking_data
    )
    apiclient.context["response"] = response


@then(parsers.parse('the response status code should be "{status_code:d}"'))
def assert_status_code(apiclient, status_code):
    """Assert that the response status code matches the expected code."""
    logger.info("Assertion of status code for update booking")
    assert (
        apiclient.context["response"].status_code == status_code
    ), f"Expected status code {status_code}, but got {apiclient.context['response'].status_code}"


@then(parsers.parse('response values should match "{recordKey}" data'))
def validate_response(apiclient, recordKey, testdata):
    """Assert that the reponse recieved for updated booking ID"""
    response_json = apiclient.context["response"].json()
    data = testdata[recordKey]
    matched = [
        data[key] == response_json[key] for key in data.keys() & response_json.keys()
    ]
    assert all(matched), "Update response does not match input payload"
