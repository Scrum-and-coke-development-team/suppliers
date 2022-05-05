Feature: The supplier service back-end
    As a Supplier
    I need a RESTful catalog service
    So that I can keep track of all my suppliers

Background:
    Given the following suppliers
    | name      | category    | available | status   |
    | supplier1 | drugs       | True      | disabled |
    | supplier2 | cosmetics   | True      | enabled  |
    | supplier3 | food        | False     | disabled |
    | supplier4 | electronics | False     | disabled |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "supplier Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Supplier
    When I visit the "Home Page"
    And I set the "id" to "12345"
    And I set the "name" to "supplier5"
    And I set the "category" to "electronics"
    And I select "True" in the "Available" dropdown
    And I select "disabled" in the "Status" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "category" field should be empty
    And the "available" field should be empty
    And the "status" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "supplier5" in the "name" field
    And I should see "electronics" in the "category" field
    And I should see "True" in the "available" dropdown
    And I should see "disabled" in the "status" dropdown

    Scenario: List all Suppliers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "supplier1" in the results
    And I should see "supplier2" in the results
    And I should not see "supplier9" in the results
    And I should see "supplier4" in the results

    Scenario: Search for Suppliers
    When I visit the "Home Page"
    And I set the "Category" to "drugs"
    And I press the "Search" button
    Then I should see "supplier1" in the results
    And I should not see "supplier2" in the results
    And I should not see "supplier3" in the results
    And I should not see "supplier4" in the results

    Scenario: Search for Suppliers
    When I visit the "Home Page"
    And I set the "Name" to "supplier2"
    And I press the "Search" button
    Then I should see "supplier2" in the results
    And I should not see "supplier1" in the results
    And I should not see "supplier3" in the results
    And I should not see "supplier4" in the results

    # Scenario: Search for Available
    # When I visit the "Home Page"
    # And I select "True" in the "Available" dropdown
    # And I press the "Search" button
    # Then I should see "supplier1" in the results
    # And I should see "supplier2" in the results
    # And I should not see "supplier3" in the results
    # And I should not see "supplier4" in the results

    Scenario: Retrieve a Supplier
    When I visit the "Home Page"
    And I set the "id" to "1234567"
    And I set the "name" to "supplier7"
    And I set the "category" to "electronics"
    And I select "True" in the "Available" dropdown
    And I select "disabled" in the "Status" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "category" field should be empty
    And the "available" field should be empty
    And the "status" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "supplier7" in the "name" field
    And I should see "electronics" in the "category" field
    And I should see "True" in the "available" dropdown
    And I should see "disabled" in the "status" dropdown
    And I should see the message "Success"

    Scenario: Delete a Supplier
    When I visit the "Home Page"
    And I set the "name" to "supplier4"
    And I set the "category" to "electronics"
    And I select "False" in the "available" dropdown
    And I select "disabled" in the "Status" dropdown
    And I press the "Search" button
    Then I should see "supplier4" in the "name" field
    And I should see "electronics" in the "category" field
    And I should see "False" in the "available" dropdown
    And I should see "disabled" in the "Status" dropdown
    When I press the "Delete" button
    Then I should see the message "Supplier has been Deleted!"
    When I set the "name" to "supplier4"
    And I press the "Search" button
    Then I should not see "supplier4" in the results
