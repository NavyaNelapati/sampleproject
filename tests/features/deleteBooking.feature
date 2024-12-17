
@deleteBooking
Feature: To delete the restful-booker booking details

  Background: create an auth token
    Given user has access to endpoint "/auth"
    And user creates a auth token with credentials

  Scenario: Delete an existing booking using Cookie Auth
    Given user has access to endpoint "/booking"
    When user send a DELETE request using "deletebookingid1" key with the token cookie
    Then the response status code should be "201"
    And the "deletebookingid1" should no longer exist in the system

  Scenario: Delete an existing booking using Basic Auth
    Given user has access to endpoint "/booking"
    When user send a DELETE request using "deletebookingid2" key with the Basic auth header
    Then the response status code should be "201"
    And the "deletebookingid2" should no longer exist in the system

  Scenario: Delete a Non-existent Booking
    Given user has access to endpoint "/booking"
    When user send a DELETE request using "invalidbookingid" key with the Basic auth header
    Then the response status code should be "405"

  Scenario: Attempt to delete a booking without authorization
    Given user has access to endpoint "/booking"
    When user send a DELETE request using "invalidbookingid" key without providing any authorization headers
    Then the response status code should be "403"

  Scenario: Attempt to delete a booking with an invalid token
    Given user has access to endpoint "/booking"
    When user send a DELETE request using "invalidbookingid" key with an invalid or expired token
    Then the response status code should be "403"
