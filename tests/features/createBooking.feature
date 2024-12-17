@createBooking
Feature: To create a new booking 

  Scenario Outline: Create a new booking with valid details
    Given user has access to endpoint "/booking"
    When user creates a booking using data "<recordKey>" from test data
    Then the response status code should be "200"
    And response should match "<recordKey>" data

    Examples: 
      | recordKey      |
      | createbooking1 |
      | createbooking2 |

  Scenario Outline: To create a new booking with checkin date later than checkout date
    Given user has access to endpoint "/booking"
    When user creates a booking using data "<recordKey>" from test data
    Then the response status code should be "500"

    Examples: 
      | recordKey          | 
      | invalidbooking1    | 
      
  Scenario Outline: To create a new booking with missing required fields
    Given user has access to endpoint "/booking"
    When user creates a booking using data "<recordKey>" from test data
    Then the response status code should be "500"

    Examples: 
      | recordKey          |
      | missingfields1     |
      | missingfields2     |


