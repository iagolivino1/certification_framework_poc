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
    common.switch_tabs(CHAT_TEMPLATE.driver, tab_title='Five9 Chat Sample')
    common.switch_to_frame(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.get_chat_frame())
    common.wait_element_attribute_contains(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.chat_content, 'innerText', reply_message)


@when("I check if the chat interaction is closed")
def check_closed_chat():
    CHAT_TEMPLATE.driver.switch_to.window(CHAT_TEMPLATE.driver.current_window_handle)
    common.switch_to_frame(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.get_chat_frame())
    try:
        common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.send_survey_button, timeout_in_seconds=5)
        # TODO: handle survey when any
    except TimeoutException:
        print("IS NOT SURVEY CONFIGURED FOR THIS CAMPAIGN?")
    common.wait_element_to_be_clickable(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.start_new_chat_button)
    print(f"WHO ENDED CHAT: {CHAT_TEMPLATE.get_end_who().text}")


@when("I close the chat interaction")
def close_chat_and_page():
    if HAS_SURVEY:
        assert CHAT_TEMPLATE.get_end_conversation_button().is_displayed(), "END CONVERSATION BUTTON IS NOT BEING DISPLAYED"
        CHAT_TEMPLATE.get_end_conversation_button().click()
        common.wait_page_element_load(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.end_chat_popup)
        CHAT_TEMPLATE.get_end_chat_popup_button().click()
    else:
        assert CHAT_TEMPLATE.get_close_conversation_button().is_displayed(), "END CONVERSATION BUTTON IS NOT BEING DISPLAYED"
        CHAT_TEMPLATE.get_close_conversation_button().click()
        common.wait_elements_to_be_less_than(CHAT_TEMPLATE.driver, CHAT_TEMPLATE.chat_frame, 1)
