from selenium.webdriver.common.by import By

import common
from page_objects.agent_home_page import AgentHomePage
from pytest_bdd import when, parsers
from step_definitions import call_interaction_steps, common_steps, chat_interaction_steps

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
    selected_channels = []
    AGENT_HOME.get_agent_status_button().click()
    AGENT_HOME.get_ready_for_option().click()
    for option in options:
        if option.lower() == 'text':
            checkbox_status = AGENT_HOME.text_channel_checkbox_status
            checkbox_path = AGENT_HOME.text_channel_checkbox
        elif option.lower() == 'voice':
            checkbox_status = AGENT_HOME.voice_channel_checkbox_status
            checkbox_path = AGENT_HOME.voice_channel_checkbox
        elif option.lower() == 'vm':
            checkbox_status = AGENT_HOME.voicemail_channel_checkbox_status
            checkbox_path = AGENT_HOME.voicemail_channel_checkbox
        else:
            raise NotImplementedError(f"NOT VALID OR NOT IMPLEMENTED OPTION: {option}")
        selected_channels.append(option)

        if "checked" not in AGENT_HOME.driver.find_element(By.XPATH, checkbox_status).get_attribute("class"):
            common.click_element(driver_=AGENT_HOME.driver, element_xpath=checkbox_path)
            common.wait_element_class_contains(AGENT_HOME.driver, checkbox_status, "checked")
    AGENT_HOME.get_confirm_channel_button().click()
    common.wait_element_class_contains(AGENT_HOME.driver, AGENT_HOME.agent_status_button, "state-ready")
    common_steps.get_agent_by_driver(AGENT_HOME.driver)['ready_channels'] = selected_channels


@when("I open agent call option")
def open_call_option():
    AGENT_HOME.get_agent_voice_button().click()
    common.wait_element_to_be_clickable(AGENT_HOME.driver, call_interaction_steps.CALL_INTERACTION_PAGE.number_input)


@when("I open agent chat option")
def open_call_option():
    AGENT_HOME.get_agent_chat_button().click()
    common.wait_element_to_be_clickable(AGENT_HOME.driver, chat_interaction_steps.CHAT_INTERACTION_PAGE.refresh_chats_button)
    chat_interaction_steps.CURRENT_NUMBER_OF_CHAT_INTERACTIONS = len(chat_interaction_steps.CHAT_INTERACTION_PAGE.get_all_chat_interactions())


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
