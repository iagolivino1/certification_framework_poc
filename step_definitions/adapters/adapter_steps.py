from pytest_bdd import when, parsers
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import Keys

import common
from page_objects.adapters.adapter_page import AdapterPage
from step_definitions import common_steps

ADAPTER_PAGE = AdapterPage()
NUMBER_OF_SELECTED_SKILLS = 0
CALL_NUMBER = ''


def handle_adapter_dnc_number():
    try:
        common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.do_not_call_dial_button)
        ADAPTER_PAGE.get_do_not_call_dial_button().click()
    except (NoSuchElementException, TimeoutException) as e:
        common.LOGGER.warning(agent=common_steps.get_agent_for_logs(), message=f"DNC dialog did not appear | {e}")


def handle_call():
    frame_name = 'SoftphoneIframe'
    ADAPTER_PAGE.driver.refresh()
    common.system_wait(5)
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.adapter_iframe)
    common.find_and_switch_to_frame(ADAPTER_PAGE.driver, frame_name)
    common.LOGGER.warning(agent=common_steps.get_agent_for_logs(), message=f'switched to frame {frame_name}')


def handle_tools_button(action='open'):
    try:
        common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.all_tools_toggle, timeout_in_seconds=5)
        tools_button = ADAPTER_PAGE.get_all_tools_toggle()
        if tools_button.text == 'More Tools':
            if action == 'open':
                tools_button.click()
        elif tools_button.text == 'Less Tools':
            if action == 'close':
                tools_button.click()
        else:
            raise Exception("TOOLS BUTTON WAS NOT PROPERLY LOADED!")
    except TimeoutException as e:
        common.LOGGER.warning(agent=common_steps.get_agent_for_logs(), message=f"tools (more | less) button was not visible at this time | exception: {e}")


@when(parsers.parse("I select {station} for adapter station type"))
def select_adt_station(station):
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.station_setup, timeout_in_seconds=120)
    common.click_element(ADAPTER_PAGE.driver, getattr(ADAPTER_PAGE, f'get_{station.lower().strip()}_station_option')())

    # check selection and try again if it fails - timeout = 5s
    is_selected = False
    for time_ in range(10):
        is_selected = getattr(ADAPTER_PAGE, f'get_{station.lower().strip()}_station_option')().get_attribute('checked') == 'true'
        if is_selected:
            break
        common.click_element(ADAPTER_PAGE.driver, getattr(ADAPTER_PAGE, f'get_{station.lower().strip()}_station_option')())
        common.system_wait(0.5)
    assert is_selected, f"STATION WAS NOT SELECTED PROPERLY: {station}"
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"station type selected: {station}")
    agent_ = common_steps.get_agent_by_driver(ADAPTER_PAGE.driver)
    agent_['station'] = station


@when(parsers.parse("I configure adapter station with {station_number} id"))
def configure_station_number(station_number):
    ADAPTER_PAGE.get_station_number_input().click()
    ADAPTER_PAGE.get_station_number_input().clear()
    ADAPTER_PAGE.get_station_number_input().send_keys(station_number)
    ADAPTER_PAGE.get_station_number_input().send_keys(Keys.TAB)
    common.click_element(ADAPTER_PAGE.driver, ADAPTER_PAGE.get_remember_my_selection_checkbox())
    common.wait_element_attribute_contains(ADAPTER_PAGE.driver, ADAPTER_PAGE.remember_my_selection_checkbox, 'checked', 'true')
    assert ADAPTER_PAGE.get_station_number_input().get_attribute('value') == station_number, f"STATION NUMBER WAS NOT SET PROPERLY: {station_number}"
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"station id filled: {station_number}")
    agent_ = common_steps.get_agent_by_driver(ADAPTER_PAGE.driver)
    agent_['station'] = {'station_type': agent_.get('station'), 'station_id': station_number}


@when("I confirm the station selection")
def confirm_selection():
    station_id = common_steps.get_agent_by_driver(ADAPTER_PAGE.driver).get('station').get('station_id')
    common.wait_element_to_be_enabled(ADAPTER_PAGE.driver, ADAPTER_PAGE.confirm_selection_button)
    ADAPTER_PAGE.get_confirm_selection_button().click()
    if common_steps.get_agent_by_driver(ADAPTER_PAGE.driver).get('station') != 'None':
        common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.content_header)
        common.wait_element_attribute_contains(ADAPTER_PAGE.driver, ADAPTER_PAGE.content_header, 'innerText', 'Station Check')
        common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.station_connection_status, timeout_in_seconds=60)
        for time_ in range(5):
            try:
                if ADAPTER_PAGE.get_confirm_selection_button().is_enabled():
                    ADAPTER_PAGE.get_confirm_selection_button().click()
                    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="station options successfully selected")
                    return
                try:
                    if "Connecting" in ADAPTER_PAGE.get_station_connection_status().text:
                        common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.reset_station_button)
                        if common.wait_element_to_be_enabled(ADAPTER_PAGE.driver, ADAPTER_PAGE.reset_station_button):
                            assert 'green' in ADAPTER_PAGE.get_station_connection_status().get_attribute('class')
                            assert 'Connected' in ADAPTER_PAGE.get_station_connection_status().get_attribute('innerText')
                            common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="station check status passed")
                            break
                except StaleElementReferenceException:
                    pass
            except (TimeoutException, AssertionError) as e:
                common.LOGGER.warning(agent=common_steps.get_agent_for_logs(),
                                      message=f"station {station_id} not connected. retry #{time_} | exception: {e}")
                if 'Assertion' not in str(e):
                    ADAPTER_PAGE.get_reset_station_button().click()
    common.wait_element_to_be_clickable(ADAPTER_PAGE.driver, ADAPTER_PAGE.confirm_selection_button, 60)
    ADAPTER_PAGE.get_confirm_selection_button().click()
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="station options successfully selected")


@when(parsers.parse("I select {skill} skill in adapter"))
def select_adt_skill(skill):
    global NUMBER_OF_SELECTED_SKILLS
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"selecting {skill} skill in adapter")
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.content_header)
    common.wait_page_element_load(ADAPTER_PAGE.driver, common_steps.COMMON_PAGE.all_skills_button, 120)
    selected_skill = None
    if skill == 'all':
        selected_skill = common_steps.COMMON_PAGE.get_all_skills_button()
    else:
        for skill_ in common_steps.COMMON_PAGE.get_available_skills():
            if skill_.text == skill:
                selected_skill = skill_
                break
    if not selected_skill.get_attribute('checked') == 'true':
        common.click_element(ADAPTER_PAGE.driver, selected_skill)
    assert selected_skill.get_attribute('checked') == 'true', f"SKILL WAS NOT SELECTED PROPERLY: {skill}"
    if skill == 'all':
        NUMBER_OF_SELECTED_SKILLS = len(common_steps.COMMON_PAGE.get_available_skills())
    else:
        NUMBER_OF_SELECTED_SKILLS += 1
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"{skill} skill selected")


@when("I confirm the skills selection")
def confirm_skills_selection():
    confirm_skills_number_label = int(ADAPTER_PAGE.get_confirm_selection_button().text.split('(')[1].replace(')', ''))
    assert confirm_skills_number_label == NUMBER_OF_SELECTED_SKILLS, \
        f"NUMBER OF SELECTED SKILLS IS NOT CORRECT IN THE BUTTON LABEL: BL: {confirm_skills_number_label} | SS: {NUMBER_OF_SELECTED_SKILLS}"
    ADAPTER_PAGE.get_confirm_selection_button().click()
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="skills selection confirmed")


@when("I see the adapter agent home page")
def see_adt_agent_home_page():
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.agent_home_panel)


@when("I select make a call option")
def select_make_a_call():
    ADAPTER_PAGE.get_make_a_call_button().click()
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.contact_call_input)


@when(parsers.parse("I fill {number} in call input number"))
def fill_call_number(number):
    global CALL_NUMBER
    ADAPTER_PAGE.get_contact_call_input().clear()
    ADAPTER_PAGE.get_contact_call_input().send_keys(number)
    ADAPTER_PAGE.get_contact_call_input().send_keys(Keys.ESCAPE)
    assert ADAPTER_PAGE.get_contact_call_input().get_attribute('value') == number, f"COULD NOT FILL THE CALL NUMBER: {number}"
    CALL_NUMBER = number
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"number {number} filled")


@when(parsers.parse("I select {campaign} campaign in adapter"))
def select_adt_campaign(campaign):
    ADAPTER_PAGE.get_select_campaign_button().click()
    common.wait_element_attribute_contains(ADAPTER_PAGE.driver, ADAPTER_PAGE.select_campaign_button, 'aria-expanded', 'true')
    selected_campaign = None
    for camp in ADAPTER_PAGE.get_campaign_options():
        if camp.get_attribute('innerText') == campaign:
            selected_campaign = camp
            break
    if not selected_campaign:
        raise Exception(f"SELECTED CAMPAIGN IS NOT AVAILABLE: {campaign}")
    common.click_element(ADAPTER_PAGE.driver, selected_campaign)
    if campaign not in ADAPTER_PAGE.get_select_campaign_button().text:
        raise Exception(f"CAMPAIGN WAS FOUND BUT COULD NOT BE SELECTED: {campaign}")
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"campaign {campaign} selected in adapter")


@when("I select dial number button")
def select_dial_number_button():
    common.wait_element_to_be_clickable(ADAPTER_PAGE.driver, ADAPTER_PAGE.dial_button)
    common.click_element(driver_=ADAPTER_PAGE.driver, element=ADAPTER_PAGE.get_dial_button())
    handle_adapter_dnc_number()
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.agent_call_panel)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="starting call...")


@when("I select dial number button on sf")
def select_dial_number_button_sf():
    common.wait_element_to_be_clickable(ADAPTER_PAGE.driver, ADAPTER_PAGE.dial_button)
    ADAPTER_PAGE.get_dial_button().click()
    handle_call()
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.agent_call_panel)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="starting call...")


@when("I select adapter script button")
def select_script_button():
    handle_tools_button(action='open')
    common.wait_element_to_be_clickable(ADAPTER_PAGE.driver, ADAPTER_PAGE.script_button)
    ADAPTER_PAGE.get_script_button().click()
    common_steps.check_new_tab()
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="script window opened")


@when("I select adapter worksheet button")
def select_worksheet_button():
    handle_tools_button(action='open')
    common.wait_element_to_be_clickable(ADAPTER_PAGE.driver, ADAPTER_PAGE.worksheet_button)
    ADAPTER_PAGE.get_worksheet_button().click()
    common_steps.check_new_tab()
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="worksheet window opened")


@when("I open adapter disposition options")
def open_adapter_dispositions():
    common.wait_element_to_be_clickable(ADAPTER_PAGE.driver, ADAPTER_PAGE.set_disposition_button)
    ADAPTER_PAGE.get_set_disposition_button().click()
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.dispositions_view)


@when(parsers.parse("I select adapter {disposition} disposition"))
def select_adapter_disposition(disposition):
    assert len(ADAPTER_PAGE.get_dispositions_list()) > 0, "NO OPTIONS IS AVAILABLE IN DISPOSITIONS LIST"
    common.click_element(ADAPTER_PAGE.driver, ADAPTER_PAGE.get_selected_disposition(text=disposition))
    assert ADAPTER_PAGE.get_selected_disposition(text=disposition).is_selected(), f"DISPOSITION WAS NOT PROPERLY SELECTED: {disposition}"
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"adapter disposition {disposition} selected")


@when("I end adapter call interaction")
def click_adapter_end_call_interaction():
    common.wait_element_to_be_clickable(ADAPTER_PAGE.driver, ADAPTER_PAGE.end_call_interaction_button)
    ADAPTER_PAGE.get_end_call_interaction_button().click()
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="adapter call ended")


@when(parsers.parse("I change adapter agent state to ready for {state}"))
def change_adapter_agent_ready_state(state):
    common.wait_element_to_be_clickable(ADAPTER_PAGE.driver, ADAPTER_PAGE.agent_state_button)
    ADAPTER_PAGE.get_agent_state_button().click()
    common.wait_element_to_be_clickable(ADAPTER_PAGE.driver, ADAPTER_PAGE.ready_for_options)
    ADAPTER_PAGE.get_ready_for_options().click()
    common.wait_element_to_be_clickable(ADAPTER_PAGE.driver, ADAPTER_PAGE.confirm_selection_button)
    if state.lower() == 'voice':
        selected_state_checkbox = ADAPTER_PAGE.get_voice_channel_checkbox()
    elif state.lower() == 'vm':
        selected_state_checkbox = ADAPTER_PAGE.get_voicemail_channel_checkbox()
    else:
        raise Exception(f"STATE OPTION NOT IMPLEMENTED: {state}")
    if not selected_state_checkbox.get_attribute('checked') == 'true':
        common.click_element(ADAPTER_PAGE.driver, selected_state_checkbox.click())
    assert selected_state_checkbox.get_attribute('checked') == 'true', f"STATE COULD NOT BE SELECTED: {state}"
    ADAPTER_PAGE.get_confirm_selection_button().click()
    common.wait_element_class_contains(ADAPTER_PAGE.driver, ADAPTER_PAGE.agent_state_button, 'btn-green')
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"agent state {state} selected")


@when("I accept the inbound call in adapter")
def accept_adapter_inbound_call():
    global CALL_NUMBER
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.inbound_call_panel)
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.active_call_type)
    common.wait_element_attribute_contains(ADAPTER_PAGE.driver, ADAPTER_PAGE.active_call_type, 'innerText', 'On Call')
    assert ADAPTER_PAGE.get_active_call_type().text.strip() == 'On Call', f"ACTIVE CALL LABEL IS NOT CORRECT: {ADAPTER_PAGE.get_active_call_type().text.strip()}"
    # update call number
    CALL_NUMBER = ADAPTER_PAGE.get_active_caller_name().text.strip()
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"call from {CALL_NUMBER} received")


@when("I accept the inbound call in SF adapter")
def accept_sf_adapter_inbound_call():
    global CALL_NUMBER
    handle_call()
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.inbound_call_panel)
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.active_call_type)
    common.wait_element_attribute_contains(ADAPTER_PAGE.driver, ADAPTER_PAGE.active_call_type, 'innerText', 'On Call')
    assert ADAPTER_PAGE.get_active_call_type().text.strip() == 'On Call', f"ACTIVE CALL LABEL IS NOT CORRECT: {ADAPTER_PAGE.get_active_call_type().text.strip()}"
    # update call number
    CALL_NUMBER = ADAPTER_PAGE.get_active_caller_name().text.strip()
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"call from {CALL_NUMBER} received")


@when("I switch to adapter Iframe")
def switch_to_iframe():
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.adapter_iframe,60)
    common.switch_to_frame(ADAPTER_PAGE.driver, ADAPTER_PAGE.get_iframe_softphone())
    common.wait_page_element_load(ADAPTER_PAGE.driver, ADAPTER_PAGE.adapter_logo)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"switched to adapter iframe")
