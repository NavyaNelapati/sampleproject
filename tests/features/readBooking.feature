@readBooking
Feature: To view the restful-booker booking details

  Scenario: To view all the booking IDs
    Given user has access to endpoint "/booking"
    When user makes a request to view booking IDs
    Then the response status code should be "200"
    And the response should contain an array of booking IDs

  Scenario: To view record by booking ID
    Given user has access to endpoint "/booking"
    When user makes a request to view booking using "readbookingid" key
    Then the response status code should be "200"
    And response should match "readbookingresponse" key

  Scenario Outline: Filter bookings by parameters
    Given user has access to endpoint "/booking"
    When user send a request to filter bookings using "<testdatakey>" key and "<index>" record
    Then the response status code should be "200"
    And the response should contain an array of booking IDs

    Examples:
        | testdatakey | index |
        | filters | 0 |
        | filters | 1 |
        | filters | 2 |
        | filters | 3 |
        | filters | 4 |
        | filters | 5 |

  Scenario Outline: Filter bookings by parameters
    Given user has access to endpoint "/booking"
    When user send a request to filter bookings by params "<filterparams>"
    Then the response status code should be "200"
    And the response should contain an empty array

    Examples:
        | filterparams |
        | {"firstname": "Unknown" } |
        | {"checkin": "9999-10-01" } |
        | {"checkout" : "9999-10-10"} |
        | {"checkout" : "01-01-2020"} |
        | {"firstname":"Unknown", "lastname": "Brown" } |
        | {"checkin": "9997-10-01", "checkout" : "9997-10-10"} |