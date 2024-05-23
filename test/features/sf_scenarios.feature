Feature: SF
    As a user,
    I want to check ADP interactions for call and chat
    So I can confirm that ADP is working fine

    Background:
        Given I set the browser number 1
        When I am in SF login page
        When I perform SF login
        When I see the SF home page

        Given I set the browser number 2
        When I am in SF login page
        When I perform SF login
        When I see the SF home page

    Scenario Outline: Check sf basic calls
        When I set the browser number 1
        And I switch to Softphone Iframe
        And I perform login
        When I select <station> for station type
        When I configure station with <station_id> id

        Examples:
        | station   | station_id      | station2  | station2_id     | inbound_number1 | inbound_number2 |
        | Softphone | 122 | WebRTC    | 870000000001202 | +18552519368    | 8552526469      |