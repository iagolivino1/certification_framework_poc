Feature: DEBUG
  As a test developer,
  I want to debug a specific scenario
  So I can confirm that the steps will work fine

  Background:
    Given I set the browser number 1
    When I am in login page
    When I perform login

  Scenario: Debug scenario
    When I select WebRTC for station type
    When I configure station with 870000000001202 id
    When I proceed to next step
    When I select all skills
    When I proceed to next step
    When I see the agent home page
    When I call +18552519368
    When I set No Disposition disposition
    Then I perform logout