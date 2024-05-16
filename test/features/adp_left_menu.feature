# Human-readable language test case
Feature: ADP left menu
  As a agent,
  I want to go to ADP home page,
  So I can check if the left menu elements are visible.

  @check_left_menu
  Scenario: Check left menu elements visibility
    Given I am in login page
    When I perform login
    When I see the home page
    When I select adp from menu
    When I check the new browser tab opened
    When I select Softphone for station type
    When I configure station with 870000000001201 id
    When I proceed to next step
    When I unselect all skills
    When I proceed to next step
    When I see the agent home page
    When I check the left menu elements visibility
    Then I perform logout