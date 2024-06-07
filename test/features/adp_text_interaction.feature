Feature: ADP text interaction
  As a user,
  I want to create new chat interaction with agent
  So I can check if agent is able to receive and answer the chat

  Background:
    Given I set the browser number 1
    When I am in login page
    When I perform login
    When I see the home page
    When I select adp from menu
    When I check the new browser tab opened

  @adp_text_interaction
  Scenario: Agent text interaction
    When I select None for station type
    When I proceed to next step
    When I select all skills
    When I proceed to next step
    When I see the agent home page
    When I change agent state to ready for text

    When I set the browser number 2
    When I go to chat template page
    When I start chat interaction
    When I fill the live chat customer information
    When I send a new message to the agent

    When I set the browser number 1
    When I open agent chat option
    When I check new chat interaction
    When I select newest chat interaction
    When I reply the chat message

    When I set the browser number 2
    When I check if agent message is displayed in customer chat

    When I set the browser number 1
    When I dispose the chat interaction

    When I set the browser number 2
    When I check if the chat interaction is closed
    Then I perform logout
