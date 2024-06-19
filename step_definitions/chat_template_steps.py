import common
from selenium.common import TimeoutException
from page_objects.chat_template_page import ChatTemplatePage
from pytest_bdd import when
from step_definitions import common_steps

CHAT_TEMPLATE = ChatTemplatePage()
HAS_SURVEY = False


@when("I go to chat template page")
def open_chat_page():
    CHAT_TEMPLATE.url = CHAT_TEMPLATE.url.replace('<chat_camp>', common_steps.get_agent_by_attributes(ready_for='text').get('chat_camp'))
    CHAT_TEMPLATE.open_page()
    common.wait_element_to_be_clickable(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.open_chat_button)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"chat console page open | url: {CHAT_TEMPLATE.url}")


@when("I start chat interaction")
def start_chat_interaction():
    CHAT_TEMPLATE.get_title_input().send_keys('Automatic chat')
    common.element_recursive_click(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.open_chat_button, 2)
    common.switch_to_frame(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.get_chat_frame())
    common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.name_input)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"chat started with title: 'Automatic chat'")


@when("I fill the live chat customer information")
def fill_customer_info():
    name, email = 'Automation Test User', 'automation@test.user'
    CHAT_TEMPLATE.get_name_input().send_keys(name)
    CHAT_TEMPLATE.get_email_input().send_keys(email)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"customer name: {name} | customer email: {email}")


@when("I send a new message to the agent")
def send_message_to_agent(start_message):
    common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.start_chat_button)
    common.system_wait(2)
    CHAT_TEMPLATE.get_question_textarea().send_keys(start_message)
    common.system_wait(2)
    CHAT_TEMPLATE.get_start_chat_button().click()
    common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.loading_message)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"message sent to agent: {start_message}")


@when("I check if agent message is displayed in customer chat")
def check_agent_message(reply_message):
    common.switch_tabs(CHAT_TEMPLATE.driver, tab_title='Five9 Chat Sample')
    common.switch_to_frame(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.get_chat_frame())
    common.wait_element_attribute_contains(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.chat_content, 'innerText', reply_message)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"agent message received: {reply_message}")


@when("I check if the chat interaction is closed")
def check_closed_chat():
    CHAT_TEMPLATE.driver.switch_to.window(CHAT_TEMPLATE.driver.current_window_handle)
    common.switch_to_frame(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.get_chat_frame())
    try:
        common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.send_survey_button, timeout_in_seconds=5)
        # TODO: handle survey when any
    except TimeoutException:
        common.LOGGER.warning(agent=common_steps.get_agent_for_logs(), message="IS NOT SURVEY CONFIGURED FOR THIS CAMPAIGN?")
    common.wait_element_to_be_clickable(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.start_new_chat_button)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="chat is closed")
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"who ended the chat: {CHAT_TEMPLATE.get_end_who().text}")


@when("I close the chat interaction")
def close_chat_and_page():
    if HAS_SURVEY:
        assert CHAT_TEMPLATE.get_end_conversation_button().is_displayed(), "END CONVERSATION BUTTON IS NOT BEING DISPLAYED"
        common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="survey flow | end conversation button found")
        CHAT_TEMPLATE.get_end_conversation_button().click()
        common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.end_chat_popup)
        CHAT_TEMPLATE.get_end_chat_popup_button().click()
    else:
        assert CHAT_TEMPLATE.get_close_conversation_button().is_displayed(), "END CONVERSATION BUTTON IS NOT BEING DISPLAYED"
        common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="close conversation button found")
        CHAT_TEMPLATE.get_close_conversation_button().click()
        common.wait_elements_to_be_less_than(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.chat_frame, 1)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="chat interaction closed/ended")
