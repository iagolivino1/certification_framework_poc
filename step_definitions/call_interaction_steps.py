import common
import driver
from pytest_bdd import parsers, when
from selenium.webdriver import Keys
from selenium.common import TimeoutException, NoSuchElementException
from page_objects.call_interaction_page import CallInteractionPage
from step_definitions import agent_steps, common_steps

CALL_INTERACTIONS = CallInteractionPage()
WORKSHEET_QUESTIONS = {}


def handle_dnc_dialog(action='accept', timeout=5, force=False):
    try:
        common.wait_element_to_be_more_than(driver_=CALL_INTERACTIONS.driver, element_xpath=CALL_INTERACTIONS.dnc_dialog,
                                            element_number=0, timeout_in_seconds=3)
        for sec in range(timeout):
            if CALL_INTERACTIONS.get_dnc_dialog().is_displayed():
                if action == 'accept':
                    CALL_INTERACTIONS.get_ok_dialog_button().click()
                else:
                    CALL_INTERACTIONS.get_cancel_dialog_button().click()
                common.system_wait(1)
                if not CALL_INTERACTIONS.get_dnc_dialog().is_displayed():
                    break
            if sec > 4 and not force:
                break
    except NoSuchElementException:
        print("DNC appeared but test could not get it!")
    except TimeoutException:
        print("DNC dialog did not appear!")


def check_script_call_tab():
    CALL_INTERACTIONS.get_script_tab().click()
    common.wait_page_element_load(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.script_content)
    call_contact_number = CALL_INTERACTIONS.get_call_contact_header().text
    common.wait_page_element_load(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.script_content)
    common.switch_to_frame(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.get_script_content())
    assert "Inbound Call Arriving!" in CALL_INTERACTIONS.get_script_title().text, "SCRIPT TITLE IS NOT BEING DISPLAYED/LOADED"
    caller_data_available = False
    for data_ in CALL_INTERACTIONS.get_script_caller_data():
        if call_contact_number == data_.text:
            caller_data_available = True
            break
    assert caller_data_available, "CALLER DATA IS NOT BEING DISPLAYED/LOADED IN SCRIPT"
    common.switch_tabs(driver_=CALL_INTERACTIONS.driver, tab_id=CALL_INTERACTIONS.driver.current_window_handle)


def check_connector_call_tab():
    # last browser tab should be the connector tab
    common.system_wait(3)
    common_steps.check_new_tab()
    assert driver.DRIVERS.get(common.get_driver_by_instance(common_steps.COMMON_PAGE.driver)).get('number_of_tabs') == \
           len(common_steps.COMMON_PAGE.driver.window_handles), "NEW TAB FOR CONNECTOR DID NOT OPEN!"
    common.wait_page_to_be_loaded(common_steps.COMMON_PAGE.driver)
    assert common_steps.COMMON_PAGE.driver.current_url == common_steps.COMMON_PAGE.connector_url, \
        f"CONNECTOR URL IS WRONG! BROWSER_URL: {common_steps.COMMON_PAGE.driver.current_url} | EXPECTED_URL: {common_steps.COMMON_PAGE.connector_url}"
    # log success


def fill_worksheet_call_tab():
    CALL_INTERACTIONS.get_worksheet_button().click()
    CALL_INTERACTIONS.get_worksheet_expand_button().click()
    # set questions
    for question_ in CALL_INTERACTIONS.get_worksheet_questions():
        WORKSHEET_QUESTIONS[question_.text.split('.')[1]] = ''

    # answer questions
    has_next_question = CALL_INTERACTIONS.get_worksheet_next_question_button().is_enabled()
    while has_next_question:
        current_question_ = CALL_INTERACTIONS.get_worksheet_current_question().text.split(')')[1]
        answer_ = f'question "{current_question_}" answer!'
        CALL_INTERACTIONS.get_worksheet_question_answer_text_area().send_keys(answer_)
        WORKSHEET_QUESTIONS[current_question_] = answer_
        has_next_question = CALL_INTERACTIONS.get_worksheet_next_question_button().is_enabled()
        if has_next_question:
            CALL_INTERACTIONS.get_worksheet_next_question_button().click()
    CALL_INTERACTIONS.get_worksheet_finish_question_button().click()


@when(parsers.parse("I select {campaign} outbound campaign"))
def select_outbound_campaign(campaign):
    CALL_INTERACTIONS.get_outbound_campaigns_button().click()
    common.wait_element_attribute_contains(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.outbound_campaigns_button, 'aria-expanded', 'true')
    available_campaigns = CALL_INTERACTIONS.get_outbound_campaigns_options()
    for campaign_ in available_campaigns:
        if campaign_.text.strip() == campaign:
            campaign_.click()
            break
    try:
        common.wait_element_attribute_contains(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.outbound_campaigns_button, 'aria-expanded', 'false')
    except TimeoutException:
        common.wait_element_attribute_to_be_not_available(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.outbound_campaigns_button, 'aria-expanded')


@when(parsers.parse("I call {number}"))
def call_number(number):
    agent_steps.AGENT_HOME.get_agent_voice_button().click()
    CALL_INTERACTIONS.get_number_input().clear()
    CALL_INTERACTIONS.get_number_input().send_keys(number)
    CALL_INTERACTIONS.get_number_input().send_keys(Keys.ESCAPE)
    CALL_INTERACTIONS.get_dial_button().click()
    handle_dnc_dialog()
    common_steps.wait_modal_dialog_open('manual', 15)
    common_steps.select_modal_next_button()
    common_steps.wait_modal_dialog_close('manual', 15)
    # log success


@when("I get the answer for the call")
def get_call_answer():
    pass


@when(parsers.parse("I check the call {tab} tab"))
@when(parsers.parse("I fill the call {tab} tab"))
def check_call_tab(tab):
    try:
        globals()['check_' + tab + '_call_tab']()
    except KeyError:
        globals()['fill_' + tab + '_call_tab']()


@when("I crosscheck the call worksheet tab answers")
def crosscheck_worksheet_answers():
    common.wait_element_attribute_contains(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.interaction_tab, 'aria-expanded', 'true')
    CALL_INTERACTIONS.get_worksheet_button().click()
    has_next_question = CALL_INTERACTIONS.get_worksheet_next_question_button().is_enabled()
    while has_next_question:
        current_question_ = CALL_INTERACTIONS.get_worksheet_current_question().text.split(')')[1]
        current_answer_ = CALL_INTERACTIONS.get_worksheet_question_answer_text_area().text
        assert current_answer_ == WORKSHEET_QUESTIONS.get(current_question_), "ANSWER WAS NOT SAVED!"
        has_next_question = CALL_INTERACTIONS.get_worksheet_next_question_button().is_enabled()
        if has_next_question:
            CALL_INTERACTIONS.get_worksheet_next_question_button().click()
    # log result


@when("I receive an inbound call")
def receive_inbound_call():
    common_steps.wait_modal_dialog_open('inbound', 60)
    common_steps.select_modal_next_button()
    common_steps.wait_modal_dialog_close('inbound', 60)  # auto-answer must be enabled
    common.wait_element_attribute_contains(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.hold_call_button, 'data-id', 'toggleHold')
    assert 'Live Call' in CALL_INTERACTIONS.get_call_voice_details_header().text, "LIVE CALL WAS NOT STARTED"



