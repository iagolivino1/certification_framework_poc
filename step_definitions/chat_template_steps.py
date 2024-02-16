import common
from page_objects.chat_template_page import ChatTemplatePage
from pytest_bdd import (
    given,
    when
)

CHAT_TEMPLATE = ChatTemplatePage()


@when("I go to chat template page")
def open_chat_page():
    CHAT_TEMPLATE.open_page()
    common.wait_element_to_be_clickable(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.open_chat_button)


@when("I start chat interaction")
def start_chat_interaction():
    CHAT_TEMPLATE.get_title_input().send_keys('Automatic chat')
    common.element_recursive_click(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.open_chat_button, 2)
    common.switch_to_frame(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.get_chat_frame())
    common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.name_input)


@when("I fill the live chat customer information")
def fill_customer_info():
    CHAT_TEMPLATE.get_name_input().send_keys('Automation Test User')
    CHAT_TEMPLATE.get_email_input().send_keys('automation@test.user')


@when("I send a new message to the agent")
def send_message_to_agent(start_message):
    common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.start_chat_button)
    common.system_wait(2)
    CHAT_TEMPLATE.get_question_textarea().send_keys(start_message)
    common.system_wait(2)
    CHAT_TEMPLATE.get_start_chat_button().click()
    common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.loading_message)


@when("I check if agent message is displayed in customer chat")
def check_agent_message(reply_message):
    CHAT_TEMPLATE.driver.switch_to.window(CHAT_TEMPLATE.driver.current_window_handle)
    common.switch_to_frame(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.get_chat_frame())
    common.system_wait(2)
    common.assert_condition(reply_message in CHAT_TEMPLATE.get_chat_content().text, "AGENT MESSAGE IS NOT BEING SENT TO CUSTOMER")


@when("I check if the chat interaction is closed")
def check_closed_chat():
    CHAT_TEMPLATE.driver.switch_to.window(CHAT_TEMPLATE.driver.current_window_handle)
    common.switch_to_frame(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.get_chat_frame())
    common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.send_survey_button)
    common.assert_condition(CHAT_TEMPLATE.get_send_survey_button().is_displayed(), "SEND SURVEY BUTTON IS NOT BEING DISPLAYED")


@when("I close the chat interaction")
def close_chat_and_page():
    common.assert_condition(CHAT_TEMPLATE.get_end_conversation_button().is_displayed(), "END CONVERSATION BUTTON IS NOT BEING DISPLAYED")
    CHAT_TEMPLATE.get_end_conversation_button().click()
    common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.end_chat_popup)
    CHAT_TEMPLATE.get_end_chat_popup_button().click()
