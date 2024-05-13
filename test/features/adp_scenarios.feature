Feature: ADP
  As a user,
  I want to check ADP interactions for call and chat
  So I can confirm that ADP is working fine

  Background:
    Given I set the browser number 1
    When I am in login page
    When I perform login
    When I see the home page
    When I select adp from menu
    When I check the second browser tab opened

    When I set the browser number 2
    When I am in login page
    When I perform login
    When I see the home page
    When I select adp from menu
    When I check the second browser tab opened

  @adp_basic_calls
  Scenario Outline: Check basic calls
    When I set the browser number 1
    When I select <station> for station type
    When I configure station with <station_id> id
    When I proceed to next step
    When I select all skills
    When I proceed to next step
    When I see the agent home page

    When I set the browser number 2
    When I select <station2> for station type
    When I configure station with <station2_id> id
    When I proceed to next step
    When I select all skills
    When I proceed to next step
    When I see the agent home page

    When I set the browser number 1
    When I open agent call option
    When I select iferreira_out outbound campaign
    When I call <inbound_number2>
    When I check the call script tab
    #When I check the call worksheet tab
    #When I check the call connector tab
    #When I set <disposition> disposition

    #When I set the browser number 2
    #When I call <inbound_number1>

    #When I set the browser number 1
    #When I receive an inbound call
    #When I check the call script tab
    #When I check the call connector tab
    #When I check the call worksheet tab
    #When I set <disposition> disposition
    Then I perform logout

  Examples:
    | station   | station_id      | station2  | station2_id     | inbound_number1 | inbound_number2 |
    | Softphone | 870000000001201 | WebRTC    | 870000000001202 | +18552519368    | 8552526469      |