from pytest_bdd import when, parsers
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys

import common
from page_objects.adt_adapter_page import ADTAdapterPage
from step_definitions import common_steps

ADT_ADAPTER_PAGE = ADTAdapterPage()
NUMBER_OF_SELECTED_SKILLS = 0


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
        raise Exception(f"NOT A VALIDATION OPTION FOR STATION: {station}")
    selected_station.click()

    # check selection and try again if it fails
    is_selected = False
    for time_ in range(10):
        is_selected = selected_station.get_attribute('checked') == 'checked'
        if is_selected:
            break
        selected_station.click()
        common.system_wait(1)
    assert is_selected, f"STATION WAS NOT SELECTED PROPERLY: {station}"


@when(parsers.parse("I configure adt station with {station_number} id"))
def configure_station_number(station_number):
    ADT_ADAPTER_PAGE.get_station_number_input().click()
    ADT_ADAPTER_PAGE.get_station_number_input().clear()
    ADT_ADAPTER_PAGE.get_station_number_input().send_keys(station_number)
    common.set_focus_out_element(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.station_number_input)
    assert ADT_ADAPTER_PAGE.get_station_number_input().value == station_number, f"STATION NUMBER WAS NOT SET PROPERLY: {station_number}"
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.content_header)
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.reset_station_button)
    common.wait_element_attribute_contains(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.content_header, 'innerText',
                                           'Station Check')
    common.wait_element_attribute_contains(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.station_connection_status, 'class',
                                           'green')
    common.wait_element_attribute_contains(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.station_connection_status,
                                           'innerText', 'Connected')


@when("I confirm the station selection")
def confirm_selection():
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
    selected_skill.click()
    assert selected_skill.checked is True, f"SKILL WAS NOT SELECTED PROPERLY: {skill}"
    if skill == 'all':
        NUMBER_OF_SELECTED_SKILLS = len(common_steps.COMMON_PAGE.get_all_skills_button())
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
    ADT_ADAPTER_PAGE.get_contact_call_input().clear()
    ADT_ADAPTER_PAGE.get_contact_call_input().send_keys(number)
    ADT_ADAPTER_PAGE.get_contact_call_input().send_keys(Keys.ESCAPE)
    assert ADT_ADAPTER_PAGE.get_contact_call_input().value == number, f"COULD NOT FILL THE CALL NUMBER: {number}"


@when(parsers.parse("I select {campaign} campaign in adt"))
def select_adt_campaign(campaign):
    ADT_ADAPTER_PAGE.get_select_campaign_button().click()
    common.wait_element_attribute_contains(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.select_campaign_button, 'aria-expanded', 'true')
    selected_campaign = None
    for camp in ADT_ADAPTER_PAGE.campaign_options:
        if camp.text == campaign:
            selected_campaign = camp
            break
    if not selected_campaign:
        raise Exception(f"SELECTED CAMPAIGN IS NOT AVAILABLE: {campaign}")
    selected_campaign.click()
    if campaign not in ADT_ADAPTER_PAGE.get_select_campaign_button().text:
        raise Exception(f"CAMPAIGN WAS FOUND BUT COULD NOT BE SELECTED: {campaign}")


@when("I select dial number button")
def select_dial_number_button():
    common.wait_element_to_be_clickable(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.dial_button)
    ADT_ADAPTER_PAGE.get_dial_button().click()
    handle_adt_dnc_number()
    common.wait_page_element_load(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.agent_call_panel)


@when("I check the call script window")
def check_call_script_window():
    handle_tools_button()
    common.wait_element_to_be_clickable(ADT_ADAPTER_PAGE.driver, ADT_ADAPTER_PAGE.script_button)
    ADT_ADAPTER_PAGE.get_script_button().click()
    # TODO: continue tomorrow
