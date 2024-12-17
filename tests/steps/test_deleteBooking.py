from pytest_bdd import scenarios, given, when, then, parsers
from tests.utils import HttpClient

import logging

logger = logging.getLogger(__name__)
# Load all scenarios from the feature file
scenarios("../features/deleteBooking.feature")


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
    context["auth_header"] = apiclient.create_auth_header()


@when(
    parsers.parse(
        'user send a DELETE request using "{deletebookingid}" key with the token cookie'
    )
)
def delete_booking_cookie_auth(apiclient, deletebookingid, context, testdata):
    """Deletes an existing booking using cookie-based authentication."""

    headers = {"Cookie": f"token={context['auth_token']}"}
    bookingid = testdata[deletebookingid]
    logger.info(
        f"Invoking delete booking scenario with cookie auth, bookingid:{bookingid}"
    )
    apiclient.set_endpoint(f"/booking/{bookingid}")
    response = apiclient.make_request(method="DELETE", headers=headers)
    apiclient.context["response"] = response


@when(
    parsers.parse(
        'user send a DELETE request using "{deletebookingid}" key with the Basic auth header'
    )
)
def delete_booking_basic_auth(apiclient, deletebookingid, context, testdata):
    """Deletes an existing booking using Basic authentication."""

    auth_header = {"Authorization": f"Basic {context['auth_header']}"}
    bookingid = testdata[deletebookingid]
    logger.info(
        f"Invoking delete booking scenario with basic auth, bookingid:{bookingid}"
    )
    apiclient.set_endpoint(f"/booking/{bookingid}")
    response = apiclient.make_request(method="DELETE", headers=auth_header)
    apiclient.context["response"] = response


@when(
    parsers.parse(
        'user send a DELETE request using "{invalidbookingid}" key without providing any authorization headers'
    )
)
def delete_booking_no_auth(apiclient, invalidbookingid, testdata):
    """Attempts to delete a booking without any authorization headers."""

    logger.info("Invoking delete booking scenario with no auth headers")
    bookingid = testdata[invalidbookingid]
    apiclient.set_endpoint(f"/booking/{bookingid}")
    response = apiclient.make_request(method="DELETE")
    apiclient.context["response"] = response


@when(
    parsers.parse(
        'user send a DELETE request using "{invalidbookingid}" key with an invalid or expired token'
    )
)
def delete_booking_invalid_token(apiclient, invalidbookingid, testdata):
    """Attempts to delete a booking using an invalid or expired token."""

    headers = {"Cookie": "token=invalidtoken"}
    bookingid = testdata[invalidbookingid]
    logger.info(f"Invoking delete booking scenario with invalid booking id:{bookingid}")
    apiclient.set_endpoint(f"/booking/{bookingid}")
    response = apiclient.make_request(method="DELETE", headers=headers)
    apiclient.context["response"] = response


@then(parsers.parse('the response status code should be "{status_code:d}"'))
def assert_status_code(apiclient, status_code):
    """Assert that the response status code matches the expected code."""

    logger.info("Assertion of status code for delete request")
    assert (
        apiclient.context["response"].status_code == status_code
    ), f"Expected status code {status_code}, but got {apiclient.context['response'].status_code}"


@then(parsers.parse('the "{deletebookingid}" should no longer exist in the system'))
def assert_booking_deleted(apiclient, deletebookingid, testdata):
    """Assert that the booking ID is no longer available in the system."""

    logger.info("Validate booking id is no longer exists")
    bookingid = testdata[deletebookingid]
    apiclient.set_endpoint(f"/booking/{bookingid}")
    response = apiclient.make_request(method="GET")
    assert response.status_code == 404
