import common
from page_objects.agent_home_page import AgentHomePage
from pytest_bdd import (
    given,
    when
)

AGENT_HOME = None


def set_pages(driver):
    # set all pages that will be used in the test
    global AGENT_HOME
    AGENT_HOME = AgentHomePage(driver)


@when("I see the agent home page")
def see_agent_home_page(driver):
    set_pages(driver)
    common.wait_element_to_be_clickable(driver, AGENT_HOME.agent_activity_button)


@when("I check the left menu elements visibility")
def check_agent_left_menu():
    common.assert_condition(AGENT_HOME.get_agent_status_button().is_displayed(), "STATUS BUTTON IS NOT VISIBLE")
    common.assert_condition(AGENT_HOME.get_agent_home_button().is_displayed(), "HOME BUTTON IS NOT VISIBLE")
    common.assert_condition(AGENT_HOME.get_agent_voice_button().is_displayed(), "CALL BUTTON IS NOT VISIBLE")
    common.assert_condition(AGENT_HOME.get_agent_voicemail_button().is_displayed(), "VOICEMAIL BUTTON IS NOT VISIBLE")


@when("I change agent state to ready for text")
def select_text_channel(driver):
    AGENT_HOME.get_agent_status_button().click()
    AGENT_HOME.get_ready_for_option().click()
    if "checked" not in AGENT_HOME.get_text_channel_checkbox_status().get_attribute("class"):
        AGENT_HOME.get_text_channel_checkbox().click()
        common.wait_element_class_contains(driver, AGENT_HOME.text_channel_checkbox, "checked")
    AGENT_HOME.get_confirm_channel_button().click()
    common.wait_element_class_contains(driver, AGENT_HOME.agent_status_button, "state-ready")


@when("Agent check and accept the text interaction")
def accept_text_interaction(driver, start_message):
    AGENT_HOME.get_agent_chat_button().click()
    common.element_recursive_click(driver, AGENT_HOME.refresh_chats_button, 15)  # 7.5s
    common.wait_element_to_be_more_than(driver, AGENT_HOME.newest_chat_interaction, 0)
    AGENT_HOME.get_unselected_lock_chat_button().click()
    AGENT_HOME.get_newest_chat_interaction().click()  # select the newest if more than 1 is displayed
    common.wait_page_element_load(driver, AGENT_HOME.conversation_content)
    common.assert_condition(start_message in AGENT_HOME.get_conversation_content().text,
                            "CUSTOMER MESSAGE IS NOT BEING SENT TO AGENT")


@when("Agent answer the message")
def reply_chat(driver, reply_message):
    common.system_wait(2)
    driver.switch_to.window(driver.current_window_handle)
    AGENT_HOME.get_reply_message_textarea().send_keys(reply_message)
    AGENT_HOME.get_send_message_button().click()


@when("Agent dispose the chat interaction")
def dispose_chat(driver):
    driver.switch_to.window(driver.current_window_handle)
    AGENT_HOME.get_set_disposition_button().click()
    common.wait_page_element_load(driver, AGENT_HOME.no_disposition_option)
    AGENT_HOME.get_no_disposition_option().click()
    common.wait_elements_to_be_less_than(driver, AGENT_HOME.newest_chat_interaction, 1)
