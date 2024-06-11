Feature: ADT+ Adapter
  As a user,
  I want to check ADT+ interactions for call and chat
  So I can confirm that ADT+ is working fine

  Background:
    Given I set the browser number 1
    When I am in adapter login page
    When I perform login in adapter

    When I set the browser number 2
    When I am in adapter login page
    When I perform login in adapter

  @adt_basic_calls
  Scenario Outline: Check ADT basic calls
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
    When I select <station2> for adapter station type
    When I configure adapter station with <station2_id> id
    When I confirm the station selection
    When I select all skill in adapter
    When I confirm the skills selection

    When I see the adapter agent home page
    When I select make a call option
    When I fill <inbound_number1> in call input number
    When I select dial number button

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
    When I open adapter disposition options
    When I select adapter No Disposition disposition
    When I end adapter call interaction

    When I perform logout in adapter

    Examples:
    | station   | station_id      | station2  | station2_id     | inbound_number1 | inbound_number2 |
    | Softphone | 660200000001164 | WebRTC    | 660200000001165 | +18882620935    | +18884343521    |
    | WebRTC    | 660200000001164 | Softphone | 660200000001165 | +18882620935    | +18884343521    |