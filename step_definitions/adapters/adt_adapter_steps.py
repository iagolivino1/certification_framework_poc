from pytest_bdd import when, parsers
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys

import common
from page_objects.adapters.adt_adapter_page import ADTAdapterPage
from step_definitions import common_steps

ADT_ADAPTER_PAGE = ADTAdapterPage()
NUMBER_OF_SELECTED_SKILLS = 0
CALL_NUMBER = ''


def handle_adt_dnc_number():
    try:
        common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.do_not_call_dial_button)
        ADT_ADAPTER_PAGE.get_do_not_call_dial_button().click()
    except NoSuchElementException:
        print("DNC dialog did not appear!")
    except TimeoutException:
        print("DNC dialog did not appear!")


def handle_tools_button(action='open'):
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.all_tools_toggle)
    tools_button = ADT_ADAPTER_PAGE.get_all_tools_toggle()
    if tools_button.text == 'More Tools':
        if action == 'open':
            tools_button.click()
    elif tools_button.text == 'Less Tools':
        if action == 'close':
            tools_button.click()
    else:
        raise Exception("TOOLS BUTTON WAS NOT PROPERLY LOADED!")


@when(parsers.parse("I select {station} for adt station type"))
def select_adt_station(station):
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.station_setup, timeout_in_seconds=120)
    if station == 'Softphone':
        selected_station = ADT_ADAPTER_PAGE.get_softphone_station_option()
    elif station == 'WebRTC':
        selected_station = ADT_ADAPTER_PAGE.get_webrtc_station_option()
    elif station == 'PSTN':
        selected_station = ADT_ADAPTER_PAGE.get_pstn_station_option()
    elif station == 'Gateway':
        selected_station = ADT_ADAPTER_PAGE.get_gateway_station_option()
    elif station == 'None':
        selected_station = ADT_ADAPTER_PAGE.get_none_station_option()
    else:
        raise Exception(f"NOT A VALID OPTION FOR STATION: {station}")
    common.click_element(ADT_ADAPTER_PAGE.driver, selected_station)

    # check selection and try again if it fails - timeout = 5s
    is_selected = False
    for time_ in range(10):
        is_selected = selected_station.get_attribute('checked') == 'true'
        if is_selected:
            break
        common.click_element(ADT_ADAPTER_PAGE.driver, selected_station)
        common.system_wait(0.5)
    assert is_selected, f"STATION WAS NOT SELECTED PROPERLY: {station}"


@when(parsers.parse("I configure adt station with {station_number} id"))
def configure_station_number(station_number):
    ADT_ADAPTER_PAGE.get_station_number_input().click()
    ADT_ADAPTER_PAGE.get_station_number_input().clear()
    ADT_ADAPTER_PAGE.get_station_number_input().send_keys(station_number)
    ADT_ADAPTER_PAGE.get_station_number_input().send_keys(Keys.TAB)
    common.click_element(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.get_remember_my_selection_checkbox())
    common.wait_element_attribute_contains(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.remember_my_selection_checkbox, 'checked', 'true')
    assert ADT_ADAPTER_PAGE.get_station_number_input().get_attribute('value') == station_number, f"STATION NUMBER WAS NOT SET PROPERLY: {station_number}"


@when("I confirm the station selection")
def confirm_selection():
    ADT_ADAPTER_PAGE.get_confirm_selection_button().click()
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.content_header)
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.reset_station_button)
    common.wait_element_attribute_contains(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.content_header, 'innerText',
                                           'Station Check')
    common.wait_element_attribute_contains(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.station_connection_status, 'class',
                                           'green')
    common.wait_element_attribute_contains(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.station_connection_status,
                                           'innerText', 'Connected')
    ADT_ADAPTER_PAGE.get_confirm_selection_button().click()


@when(parsers.parse("I select {skill} skill in adt"))
def select_adt_skill(skill):
    global NUMBER_OF_SELECTED_SKILLS
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.content_header)
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, common_steps.COMMON_PAGE.all_skills_button)
    selected_skill = None
    if skill == 'all':
        selected_skill = common_steps.COMMON_PAGE.get_all_skills_button()
    else:
        for skill_ in common_steps.COMMON_PAGE.get_available_skills():
            if skill_.text == skill:
                selected_skill = skill_
                break
    if not selected_skill.get_attribute('checked') == 'true':
        common.click_element(ADT_ADAPTER_PAGE.driver, selected_skill)
    assert selected_skill.get_attribute('checked') == 'true', f"SKILL WAS NOT SELECTED PROPERLY: {skill}"
    if skill == 'all':
        NUMBER_OF_SELECTED_SKILLS = len(common_steps.COMMON_PAGE.get_available_skills())
    else:
        NUMBER_OF_SELECTED_SKILLS += 1


@when("I confirm the skills selection")
def confirm_skills_selection():
    confirm_skills_number_label = int(ADT_ADAPTER_PAGE.get_confirm_selection_button().text.split('(')[1].replace(')', ''))
    assert confirm_skills_number_label == NUMBER_OF_SELECTED_SKILLS, \
        f"NUMBER OF SELECTED SKILLS IS NOT CORRECT IN THE BUTTON LABEL: BL: {confirm_skills_number_label} | SS: {NUMBER_OF_SELECTED_SKILLS}"
    ADT_ADAPTER_PAGE.get_confirm_selection_button().click()


@when("I see the adt agent home page")
def see_adt_agent_home_page():
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.agent_home_panel)


@when("I select make a call option")
def select_make_a_call():
    ADT_ADAPTER_PAGE.get_make_a_call_button().click()
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.contact_call_input)


@when(parsers.parse("I fill {number} in call input number"))
def fill_call_number(number):
    global CALL_NUMBER
    ADT_ADAPTER_PAGE.get_contact_call_input().clear()
    ADT_ADAPTER_PAGE.get_contact_call_input().send_keys(number)
    ADT_ADAPTER_PAGE.get_contact_call_input().send_keys(Keys.ESCAPE)
    assert ADT_ADAPTER_PAGE.get_contact_call_input().get_attribute('value') == number, f"COULD NOT FILL THE CALL NUMBER: {number}"
    CALL_NUMBER = number


@when(parsers.parse("I select {campaign} campaign in adt"))
def select_adt_campaign(campaign):
    ADT_ADAPTER_PAGE.get_select_campaign_button().click()
    common.wait_element_attribute_contains(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.select_campaign_button, 'aria-expanded', 'true')
    selected_campaign = None
    for camp in ADT_ADAPTER_PAGE.get_campaign_options():
        if camp.get_attribute('innerText') == campaign:
            selected_campaign = camp
            break
    if not selected_campaign:
        raise Exception(f"SELECTED CAMPAIGN IS NOT AVAILABLE: {campaign}")
    common.click_element(ADT_ADAPTER_PAGE.driver, selected_campaign)
    if campaign not in ADT_ADAPTER_PAGE.get_select_campaign_button().text:
        raise Exception(f"CAMPAIGN WAS FOUND BUT COULD NOT BE SELECTED: {campaign}")


@when("I select dial number button")
def select_dial_number_button():
    common.wait_element_to_be_clickable(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.dial_button)
    ADT_ADAPTER_PAGE.get_dial_button().click()
    handle_adt_dnc_number()
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.agent_call_panel)


@when("I select adt script button")
def select_script_button():
    handle_tools_button(action='open')
    common.wait_element_to_be_clickable(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.script_button)
    ADT_ADAPTER_PAGE.get_script_button().click()
    common_steps.check_new_tab()


@when("I select adt worksheet button")
def select_script_button():
    handle_tools_button(action='open')
    common.wait_element_to_be_clickable(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.worksheet_button)
    ADT_ADAPTER_PAGE.get_worksheet_button().click()
    common_steps.check_new_tab()


@when("I open adt disposition options")
def open_adapter_dispositions():
    common.wait_element_to_be_clickable(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.set_disposition_button)
    ADT_ADAPTER_PAGE.get_set_disposition_button().click()
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.dispositions_view)


@when(parsers.parse("I select adt {disposition} disposition"))
def select_adapter_disposition(disposition):
    assert len(ADT_ADAPTER_PAGE.get_dispositions_list()) > 0, "NO OPTIONS IS AVAILABLE IN DISPOSITIONS LIST"
    ADT_ADAPTER_PAGE.get_selected_disposition(text=disposition).click()
    assert ADT_ADAPTER_PAGE.get_selected_disposition(text=disposition).is_selected(), f"DISPOSITION WAS NOT PROPERLY SELECTED: {disposition}"


@when("I end adapter call interaction")
def click_adapter_end_call_interaction():
    common.wait_element_to_be_clickable(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.end_call_interaction_button)
    ADT_ADAPTER_PAGE.get_end_call_interaction_button().click()


@when(parsers.parse("I change adt agent state to ready for {state}"))
def change_adapter_agent_ready_state(state):
    ADT_ADAPTER_PAGE.get_agent_state_button().click()
    common.wait_element_to_be_clickable(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.ready_for_options)
    ADT_ADAPTER_PAGE.get_ready_for_options().click()
    common.wait_element_to_be_clickable(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.confirm_selection_button)
    if state.lower() == 'voice':
        selected_state_checkbox = ADT_ADAPTER_PAGE.get_voice_channel_checkbox()
    elif state.lower() == 'vm':
        selected_state_checkbox = ADT_ADAPTER_PAGE.get_voicemail_channel_checkbox()
    else:
        raise Exception(f"STATE OPTION NOT IMPLEMENTED: {state}")
    if not selected_state_checkbox.get_attribute('checked') == 'true':
        common.click_element(ADT_ADAPTER_PAGE.driver, selected_state_checkbox.click())
    assert selected_state_checkbox.get_attribute('checked') == 'true', f"STATE COULD NOT BE SELECTED: {state}"


@when("I accept the inbound call in adt")
def accept_adapter_inbound_call():
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.inbound_call_panel)
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.active_call_type)
    assert ADT_ADAPTER_PAGE.get_active_call_type().text == 'On Call'
