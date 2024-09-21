Feature: Sentiment Analysis Application
    As a User
    I need a web application that performs sentiment analysis
    So that I can understand the sentiment of my text input

Background:
    Given the application is running

Scenario: Analyze Sentiment
    When I visit the "Home Page"
    And I enter "I love Flask" in the input field
    And I press the "Analyze" button
    Then I should see "POSITIVE" as the sentiment result

Scenario: Handle Empty Input
    When I visit the "Home Page"
    And I press the "Analyze" button
    Then I should see an error message "Text is required"

Scenario: Analyze Negative Sentiment
    When I visit the "Home Page"
    And I enter "I hate bugs" in the input field
    And I press the "Analyze" button
    Then I should see "NEGATIVE" as the sentiment result

Scenario: Analyze Neutral Sentiment
    When I visit the "Home Page"
    And I enter "This is a sentence." in the input field
    And I press the "Analyze" button
    Then I should see "NEUTRAL" as the sentiment result

Scenario: Analyze Mixed Sentiment
    When I visit the "Home Page"
    And I enter "I love Python but hate Java." in the input field
    And I press the "Analyze" button
    Then I should see "MIXED" as the sentiment result
