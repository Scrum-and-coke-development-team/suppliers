Feature: The supplier service back-end
    As a Supplier
    I need a RESTful catalog service
    So that I can keep track of all my suppliers

Background:
    Given the following suppliers
        | name       | category    | availability |
        | supplier1  | drugs       | true         |
        | supplier2  | cosmetics   | true         |
        | supplier3  | food        | false        |
        | supplier4  | electronics | true         |


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Supplier Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Supplier
    When I visit the "Home Page"
    And I set the "name" to "supplier4"
    And I set the "category" to "electronics"
    And I select "false" in the "availability" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "category" field should be empty
    And the "availability" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "supplier4" in the "name" field
    And I should see "electronics" in the "category" field
    And I should see "False" in the "availability" dropdown


    Scenario: List all Suppliers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "supplier1" in the results
    And I should see "supplier2" in the results
    And I should not see "supplier3" in the results
    And I should see "supplier4" in the results


    Scenario: Update a Supplier
    When I visit the "Home Page"
    And I set the "name" to "supplier1"
    And I press the "Search" button
    Then I should see "supplier1" in the "name" field
    And I should see "drugs" in the "category" field
    And I should see "true" in the "availability" dropdown
    When I change "name" to "supplier4"
    And I change "category" to "food"
    And I select "true" in the "availability" dropdown 
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "supplier4" in the "name" field
    And I should see "food" in the "category" field
    And I should see "true" in the "availability" dropdown
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "supplier4" in the results
    And I should not see "supplier1" in the results