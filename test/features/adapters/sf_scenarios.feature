Feature: SF
    As a user,
    I want to check ADP interactions for call and chat
    So I can confirm that ADP is working fine

    Background:
        Given I set the browser number 1
        When I am in SF login page
        When I perform SF login
        When I see the SF home page
        And I switch to adapter Iframe
        And I perform login in adapter

        When I set the browser number 2
        When I am in login page
        When I perform login
        When I see the home page
        When I select adp from menu
        When I check the new browser tab opened

    Scenario Outline: Check sf basic calls
        When I set the browser number 1
        And I switch to adapter Iframe
        When I select <station> for adapter station type
        When I configure adapter station with <station_id> id
        When I confirm the station selection
        When I proceed to next step
        When I select all skill in adapter
        When I see the adapter agent home page
        When I select make a call option
        When I fill <inbound_number2> in call input number
        When I select cert_out campaign in adapter
        When I select dial number button on sf
        When I select adapter script button
        When I check the call script window
        When I close the current browser tab
        And I switch to adapter Iframe
        When I select adapter worksheet button
        When I check the call worksheet window
        When I fill the adapter worksheet
        And I switch to adapter Iframe
        When I select adapter worksheet button
        When I check the call worksheet window
        When I close the current browser tab
        And I switch to adapter Iframe
        When I open adapter disposition options
        When I select adapter No Disposition disposition
        When I end adapter call interaction
        When I check the call connector tab
        When I close the current browser tab
        And I switch to adapter Iframe
        When I change adapter agent state to ready for voice


        When I set the browser number 2
        When I select <station2> for station type
        When I configure station with <station2_id> id
        When I proceed to next step
        When I select all skills
        When I proceed to next step
        When I see the agent home page
        When I call <inbound_number1>

        When I set the browser number 1
        When I accept the inbound call in SF adapter
        When I select adapter script button
        When I check the call script window
        When I close the current browser tab
        And I switch to adapter Iframe
        When I select adapter worksheet button
        When I check the call worksheet window
        When I fill the adapter worksheet
        And I switch to adapter Iframe
        When I select adapter worksheet button
        When I check the call worksheet window
        When I close the current browser tab
        And I switch to adapter Iframe
        When I open adapter disposition options
        When I select adapter No Disposition disposition
        When I end adapter call interaction
        When I check the call connector tab
        When I close the current browser tab
        And I switch to adapter Iframe

        When I set the browser number 2
        When I set No Disposition disposition

        When I perform logout in adapter
        Then I perform logout   

        Examples:
        | station   | station_id      | station2  | station2_id     | inbound_number1 | inbound_number2 |
        | Softphone | 660200000001160 | WebRTC    | 660200000001161 | 8882620935     | 8884343521    |
        # | Softphone | 660200000001161 | WebRTC    | 660200000001160 | 8882620935     | 8884343521    |
        # | Softphone | 870000000001201 | WebRTC    | 870000000001202 | +18552519368    | 8552526469      |
        # | Softphone | 32              | WebRTC    | 36              | 8669157428      | 9255748216      |
        # | Softphone | 870000000001202 | WebRTC    | 870000000001201 | +18552519368    | 8552526469      |