Feature: DEBUG
  As a test developer,
  I want to debug a specific scenario
  So I can confirm that the steps will work fine

  Background:
    Given I set the browser number 1
    When I am in login page

  Scenario: Debug scenario
    When I perform login
    When I see the home page

    # debug inbound campaign number: +18669157123