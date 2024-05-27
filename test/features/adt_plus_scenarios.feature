Feature: ADT+ Adapter
  As a user,
  I want to check ADT+ interactions for call and chat
  So I can confirm that ADT+ is working fine

  Background:
    Given I set the browser number 1

  Scenario: Login ADT
    When I am in adt login page
    When I perform login
    When I select Softphone for adt station type
    When I configure adt station with 870000000001201 id
    When I confirm the station selection
    When I select all skill in adt
    When I confirm the skills selection

    When I see the adt agent home page
    When I select make a call option
    When I fill <inbound_number2> in call input number
    When I select iferreira_out campaign in adt
    When I select dial number button
    When I check the call script window
    When I check the call worksheet window
    When I fill the worksheet
    When I check the call worksheet window
    When I open disposition options
    When I select No Disposition disposition
    When I check the call connector tab

    When I switch to adapter tab
    When I change adt agent state to ready for voice

    When I set the browser number 2
    When I call <inbound_number1>

    When I set the browser number 1
    When I accept the inbound call in adt
    When I check the call script window
    When I check the call worksheet window
    When I fill the worksheet
    When I check the call worksheet window
    When I open disposition options
    When I select No Disposition disposition
    When I check the call connector tab

    When I set the browser number 2
    When I set No Disposition disposition

    When I perform logout in adt
    Then I perform logout