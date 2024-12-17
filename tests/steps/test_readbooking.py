from pytest_bdd import scenarios, given, when, then, parsers
from tests.utils import HttpClient
import json

import logging

logger = logging.getLogger(__name__)
# Load all scenarios from the feature file
scenarios("../features/readBooking.feature")


@given(
    parsers.parse('user has access to endpoint "{endpoint}"'),
    target_fixture="apiclient",
)
def create_client(endpoint):
    client = HttpClient(endpoint)
    client.context = {}
    return client


@when(parsers.parse("user makes a request to view booking IDs"))
def get_booking_ids(apiclient):
    """Retreive all booking ids """
    logger.info("Invoking read booking scenario to view all ids")
    response = apiclient.make_request(method="GET")
    apiclient.context["response"] = response


@when(parsers.parse('user makes a request to view booking using "{readbookingid}" key'))
def get_one_booking(apiclient, readbookingid, testdata):
    """Retreive one booking ids """
    bookingid = testdata[readbookingid]
    logger.info(f"Invoking read booking scenario to view one booking: {bookingid}")
    apiclient.set_endpoint(f"booking/{bookingid}")
    response = apiclient.make_request(method="GET")
    apiclient.context["response"] = response


@when(
    parsers.parse(
        'user send a request to filter bookings using "{testdatakey}" key and "{index}" record'
    )
)
def filter_booking(apiclient, testdatakey, index, testdata):
    """filter bookingids based on parameters"""
    logger.info("Invoking read booking scenario based on filters")
    filter_params_dict = json.loads(testdata[testdatakey][index])
    response = apiclient.make_request(method="GET", params=filter_params_dict)
    apiclient.context["response"] = response


@when(
    parsers.parse('user send a request to filter bookings by params "{filterparams}"')
)
def filter_booking_invalid(filterparams, apiclient):
    """filter bookingids based on invalid parameters"""
    logger.info("Invoking read booking scenario based on invalid filters")
    filter_params_dict = json.loads(filterparams)
    response = apiclient.make_request(method="GET", params=filter_params_dict)
    apiclient.context["response"] = response


@then(parsers.parse('the response status code should be "{status_code:d}"'))
def assert_status_code(apiclient, status_code):
    """Assert that the response status code matches the expected code."""
    logger.info("Assertion of status code for read request")
    assert (
        apiclient.context["response"].status_code == status_code
    ), f"Expected status code {status_code}, but got {apiclient.context['response'].status_code}"


@then('the response should contain an array of booking IDs')
def assert_booking_response_nonempty(apiclient):
    """Assertion to validate booking response has atleast one record"""
    logger.info("Assertion of non-empty response for read booking")
    response = apiclient.context.get("response").json()
    assert len(response) > 0, f"Expected atleast one record, recieved 0 records"


@then(parsers.parse('the response should contain an empty array'))
def assert_booking_response_empty(apiclient):
    """Assertion to validate booking response empty scenario"""
    logger.info("Assertion of empty response for read booking")
    response = apiclient.context.get("response").json()
    assert len(response) == 0, f"Expected empty response, recieved:{len(response)} records"


@then(parsers.parse('response should match "{readbookingresponse}" key'))
def validate_response(apiclient, readbookingresponse, testdata):
    """Assert that the reponse recieved for read booking ID"""
    response_json = apiclient.context["response"].json()
    data = testdata["readbookingresponse"]
    matched = [
        data[key] == response_json[key] for key in data.keys() & response_json.keys()
    ]
    assert all(matched), "read response does not match input payload"
