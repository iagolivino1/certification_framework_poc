Feature: DEBUG
  As a test developer,
  I want to debug a specific scenario
  So I can confirm that the steps will work fine

  Background:
    Given I set the browser number 1
    When I am in direct login page
    When I perform login

  Scenario: Debug scenario
    When I select Softphone for station type
    When I configure station with 660200000001164 id
    When I proceed to next step
    When I select all skills
    When I proceed to next step
    When I see the agent home page
    When I change agent state to ready for voice

    Then I perform logout