Feature: Chat interaction
  As a user,
  I want to create new chat interaction with agent
  So I can check if agent is able to receive chat

  @check_text_interaction
  Scenario: Check agent text interaction
    Given I am in login page
    When I perform login
    When I see the home page
    When I select adp from menu
    When I check the new browser tab opened
    When I select None for station type
    When I proceed to next step
    When I select all skills
    When I proceed to next step
    When I see the agent home page
    When I change agent state to ready for text
    When I go to chat template page
    When I start chat interaction
    When I fill the live chat customer information
    When I send a new message to the agent
    When Agent check and accept the text interaction
    When Agent answer the message
    When I check if agent message is displayed in customer chat
    When Agent dispose the chat interaction
    When I check if the chat interaction is closed
    Then I perform logout
