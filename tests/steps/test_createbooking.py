from pytest_bdd import scenarios, given, when, then, parsers
from tests.utils import HttpClient

import logging

logger = logging.getLogger(__name__)
# Load all scenarios from the feature file
scenarios("../features/createBooking.feature")


@given(
    parsers.parse('user has access to endpoint "{endpoint}"'),
    target_fixture="apiclient",
)
def create_client(endpoint):
    client = HttpClient(endpoint)
    client.context = {}
    return client


@when(parsers.parse('user creates a booking using data "{recordKey}" from test data'))
def create_booking(apiclient, recordKey, testdata):
    """Creates a booking using the data from the testdata and key."""
    # Load booking data from the file
    logger.info("Invoking create booking scenario")
    booking_data = testdata[recordKey]
    # Make the POST request to create a booking
    response = apiclient.make_request(method="POST", payload=booking_data)
    apiclient.context = {"response": response}


@then(parsers.parse('the response status code should be "{status_code:d}"'))
def assert_status_code(apiclient, status_code):
    """Assert that the response status code matches the expected code."""
    logger.info("Assertion of status code for create request")
    assert (
        apiclient.context["response"].status_code == status_code
    ), f"Expected status code {status_code}, but got {apiclient.context['response'].status_code}"


@then(parsers.parse('response should match "{recordkey}" data'))
def validate_response(apiclient, recordkey, testdata):
    """Validates the response against a input payload."""
    logger.info("validate response recieved from api")
    response_json = apiclient.context["response"].json()
    data = testdata[recordkey]
    matched = [
        data[key] == response_json[key] for key in data.keys() & response_json.keys()
    ]
    assert all(matched), "create response does not match input payload"
