import common
from page_objects.agent_home_page import AgentHomePage
from pytest_bdd import when, parsers
from step_definitions import call_interaction_steps

AGENT_HOME = AgentHomePage()


@when("I see the agent home page")
def see_agent_home_page():
    common.wait_element_to_be_clickable(AGENT_HOME.driver, AGENT_HOME.agent_activity_button)


@when("I check the left menu elements visibility")
def check_agent_left_menu():
    common.assert_condition(AGENT_HOME.get_agent_status_button().is_displayed(), "STATUS BUTTON IS NOT VISIBLE")
    common.assert_condition(AGENT_HOME.get_agent_home_button().is_displayed(), "HOME BUTTON IS NOT VISIBLE")
    common.assert_condition(AGENT_HOME.get_agent_voice_button().is_displayed(), "CALL BUTTON IS NOT VISIBLE")
    common.assert_condition(AGENT_HOME.get_agent_voicemail_button().is_displayed(), "VOICEMAIL BUTTON IS NOT VISIBLE")


@when(parsers.parse("I change agent state to ready for {options}"))
def set_agent_ready_for(options):
    common.switch_tabs(AGENT_HOME.driver, tab_title='Agent Desktop Plus')
    options = options.split(',')
    AGENT_HOME.get_agent_status_button().click()
    AGENT_HOME.get_ready_for_option().click()
    for option in options:
        if option.lower() == 'text':
            checkbox = AGENT_HOME.get_text_channel_checkbox()
            checkbox_status = AGENT_HOME.get_text_channel_checkbox_status()
            checkbox_path = AGENT_HOME.text_channel_checkbox
        elif option.lower() == 'voice':
            checkbox = AGENT_HOME.get_voice_channel_checkbox()
            checkbox_status = AGENT_HOME.get_voice_channel_checkbox_status()
            checkbox_path = AGENT_HOME.voice_channel_checkbox
        elif option.lower() == 'vm':
            checkbox = AGENT_HOME.get_voicemail_channel_checkbox()
            checkbox_status = AGENT_HOME.get_voicemail_channel_checkbox_status()
            checkbox_path = AGENT_HOME.voicemail_channel_checkbox
        else:
            raise NotImplementedError(f"NOT VALID OR NOT IMPLEMENTED OPTION: {option}")

        if "checked" not in checkbox_status.get_attribute("class"):
            checkbox.click()
            common.wait_element_class_contains(AGENT_HOME.driver, checkbox_path, "checked")
    AGENT_HOME.get_confirm_channel_button().click()
    common.wait_element_class_contains(AGENT_HOME.driver, AGENT_HOME.agent_status_button, "state-ready")


@when("Agent check and accept the text interaction")
def accept_text_interaction(start_message):
    AGENT_HOME.get_agent_chat_button().click()
    common.element_recursive_click(AGENT_HOME.driver, AGENT_HOME.refresh_chats_button, 15)  # 7.5s
    common.wait_element_to_be_more_than(AGENT_HOME.driver, AGENT_HOME.newest_chat_interaction, 0)
    AGENT_HOME.get_unselected_lock_chat_button().click()
    AGENT_HOME.get_newest_chat_interaction().click()  # select the newest if more than 1 is displayed
    common.wait_page_element_load(AGENT_HOME.driver, AGENT_HOME.conversation_content)
    common.assert_condition(start_message in AGENT_HOME.get_conversation_content().text,
                            "CUSTOMER MESSAGE IS NOT BEING SENT TO AGENT")


@when("Agent answer the message")
def reply_chat(reply_message):
    common.system_wait(2)
    AGENT_HOME.driver.switch_to.window(AGENT_HOME.driver.current_window_handle)
    AGENT_HOME.get_reply_message_textarea().send_keys(reply_message)
    AGENT_HOME.get_send_message_button().click()


@when("Agent dispose the chat interaction")
def dispose_chat():
    AGENT_HOME.driver.switch_to.window(AGENT_HOME.driver.current_window_handle)
    AGENT_HOME.get_set_disposition_button().click()
    common.wait_page_element_load(AGENT_HOME.driver, AGENT_HOME.no_disposition_option)
    AGENT_HOME.get_no_disposition_option().click()
    common.wait_elements_to_be_less_than(AGENT_HOME.driver, AGENT_HOME.newest_chat_interaction, 1)


@when("I open agent call option")
def open_call_option():
    AGENT_HOME.get_agent_voice_button().click()
    common.wait_element_to_be_clickable(AGENT_HOME.driver, call_interaction_steps.CALL_INTERACTION_PAGE.number_input)


@when(parsers.parse("I set {disposition} disposition"))
def set_disposition(disposition):
    common.system_wait(5)
    AGENT_HOME.get_set_disposition_button().click()
    # a way to define which element xpath and attribute should be used
    dropdown_details = [AGENT_HOME.set_disposition_button, 'aria-expanded', 'true']
    if common.TEST_INFO.get('lab') == 'qa02':
        dropdown_details = [f"{dropdown_details[0]}/..", 'class', 'open']  # up one more level to get the button parent's
    common.wait_element_attribute_contains(AGENT_HOME.driver, dropdown_details[0], dropdown_details[1], dropdown_details[2])
    if disposition == 'No Disposition':
        AGENT_HOME.get_no_disposition_option().click()
    elif disposition == 'Do Not Call':
        AGENT_HOME.get_do_not_call_disposition_option().click()
    else:
        for disposition_ in AGENT_HOME.get_all_dispositions():
            if disposition_.text == disposition:
                disposition_.click()
                break
    common.wait_page_element_load(AGENT_HOME.driver, call_interaction_steps.CALL_INTERACTION_PAGE.number_input)
