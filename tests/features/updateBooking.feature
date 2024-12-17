@updateBooking
Feature: To update a booking in restful-booker

  Background: create an auth token
    Given user has access to endpoint "/auth"
    And user creates a auth token with credentials

  Scenario Outline: Update an existing booking
    Given user has access to endpoint "/booking"
    When user send a "PUT" to "updatebookingid" using data "<recordKey>" from test data
    Then the response status code should be "200"
    And response values should match "<recordKey>" data

    Examples: 
      | recordKey           |
      | updatebooking1      |
      | updatebooking2      |

  Scenario Outline: Update an expired booking
    Given user has access to endpoint "/booking"
    When user send a "PUT" to "expiredbookingid" using data "<recordKey>" from test data
    Then the response status code should be "400"

    Examples: 
      | recordKey        |
      | expiredbooking1 |

  Scenario Outline: Partial Update an existing booking
    Given user has access to endpoint "/booking"
    When user send a "PATCH" to "updatebookingid" using data "<recordKey>" from test data
    Then the response status code should be "200"
    And response values should match "<recordKey>" data

    Examples: 
      | recordKey        |
      | partialUpdatebooking1 |
      | partialUpdatebooking2 |
    
  Scenario Outline: Partial Update an expired booking
    Given user has access to endpoint "/booking"
    When user send a "PATCH" to "expiredbookingid" using data "<recordKey>" from test data
    Then the response status code should be "400"

    Examples: 
      | recordKey        |
      | partialUpdatebooking1 |