Feature: NetSuite Adapter
  As a user,
  I want to check NetSuite interactions for call and chat
  So I can confirm that NetSuite is working fine

  Background:
    Given I set the browser number 1
    When I am in NetSuite login page
    When I perform NetSuite login
    When I see the NetSuite home page
    When I launch the adapter
    When I am in adapter login page
    When I perform login in adapter

    When I set the browser number 2
    When I am in login page
    When I perform login
    When I see the home page
    When I select adp from menu
    When I check the new browser tab opened

  @adt_basic_calls
  Scenario Outline: Check NetSuite basic calls
    When I set the browser number 1
    When I select <station> for adapter station type
    When I configure adapter station with <station_id> id
    When I confirm the station selection
    When I select all skill in adapter
    When I confirm the skills selection

    When I see the adapter agent home page
    When I select make a call option
    When I fill <inbound_number2> in call input number
    When I select cert_out campaign in adapter
    When I select dial number button
    When I select adapter script button
    When I check the call script window
    When I close the current browser tab
    When I switch to tab with Adapter title
    When I select adapter worksheet button
    When I check the call worksheet window
    When I fill the adapter worksheet
    When I switch to tab with Adapter title
    When I select adapter worksheet button
    When I check the call worksheet window
    When I close the current browser tab
    When I switch to tab with Adapter title
    When I open adapter disposition options
    When I select adapter No Disposition disposition
    When I end adapter call interaction
    When I check the call connector tab
    When I close the current browser tab

    When I switch to tab with Adapter title
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
    When I accept the inbound call in adapter
    When I select adapter script button
    When I check the call script window
    When I close the current browser tab
    When I switch to tab with Adapter title
    When I select adapter worksheet button
    When I check the call worksheet window
    When I fill the adapter worksheet
    When I switch to tab with Adapter title
    When I select adapter worksheet button
    When I check the call worksheet window
    When I close the current browser tab
    When I switch to tab with Adapter title
    When I open adapter disposition options
    When I select adapter No Disposition disposition
    When I end adapter call interaction
    When I check the call connector tab
    When I close the current browser tab
    When I switch to tab with Adapter title

    When I set the browser number 2
    When I set No Disposition disposition

    When I perform logout in adapter
    Then I perform logout  

    Examples:
    | station   | station_id      | station2  | station2_id     | inbound_number1 | inbound_number2 |
    | Softphone | 660200000001164 | WebRTC    | 660200000001165 | +18882620935    | +18884343521    |