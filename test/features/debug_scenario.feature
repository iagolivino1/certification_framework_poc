Feature: DEBUG
  As a test developer,
  I want to debug a specific scenario
  So I can confirm that the steps will work fine

  Background:
    Given I set the browser number 1
    When I am in adapter login page
    When I perform login in adapter

  Scenario: Debug scenario
    When I select Softphone for adapter station type
    When I configure adapter station with 660200000001164 id
    When I confirm the station selection
    When I select all skill in adapter
    When I confirm the skills selection

    When I see the adapter agent home page
    When I select make a call option
    When I fill +18884343521 in call input number
    When I select cert_out campaign in adapter
    ##When I select dial number button
    When I select dial number button

    When I open adapter disposition options
    When I select adapter No Disposition disposition
    When I end adapter call interaction
    When I check the call connector tab
    When I close the current browser tab

    Then I perform logout in adapter

    # debug inbound campaign number: +18669157123