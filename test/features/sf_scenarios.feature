Feature: SF
    As a user,
    I want to check ADP interactions for call and chat
    So I can confirm that ADP is working fine

    Background:
        Given I set the browser number 1
        When I am in SF login page
        When I perform SF login
        When I see the SF home page

        # Given I set the browser number 2
        # When I am in SF login page
        # When I perform SF login
        # When I see the SF home page

    Scenario Outline: Check sf basic calls
        When I set the browser number 1
        And I switch to Softphone Iframe
        And I perform login
        When I select <station> for adapter station type
        When I configure adapter station with <station_id> id
        When I proceed to next step
        When I select all skills on SF
        When I proceed to next step
        When I see the SF agent logged in
        
        When I set the browser number 1
        When I open agent call option
        When I select ds_out1 outbound campaign
        When I call <inbound_number2> from adapter
        When I check the call adapter script tab
        When I fill the call adapter worksheet tab
        When I crosscheck the call adapter worksheet tab answers
        When I set Done disposition on adapter
        # When I check the call connector tab
        # When I close the current browser tab
        When I change agent state to ready for voice on adapter

        # When I set the browser number 2
        # And I switch to Softphone Iframe
        # And I perform login
        # When I select <station2> for adapter station type
        # When I configure adapter station with <station2_id> id
        # When I proceed to next step
        # When I select all skills on SF
        # When I proceed to next step
        # When I see the agent SF home page

        Examples:
        | station   | station_id      | station2  | station2_id     | inbound_number1 | inbound_number2 |
        | Softphone | 37              | WebRTC    | 36              | 8552526469      | 9255748216      |
        # | Softphone | 870000000001202 | WebRTC    | 870000000001201 | +18552519368    | 8552526469      |