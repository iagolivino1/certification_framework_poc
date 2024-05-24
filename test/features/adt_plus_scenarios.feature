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