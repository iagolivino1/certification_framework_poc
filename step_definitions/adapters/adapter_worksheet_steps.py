import common
from pytest_bdd import when
from page_objects.adapters.adapter_worksheet_page import AdapterWorksheetPage
from step_definitions import common_steps

ADAPTER_WORKSHEET_PAGE = AdapterWorksheetPage()
WORKSHEET_QUESTIONS = {}


@when("I check the call worksheet window")
def check_worksheet_window():
    global WORKSHEET_QUESTIONS
    assert 'Five9 Adapter - Worksheet' in ADAPTER_WORKSHEET_PAGE.driver.title, "WORKSHEET WINDOW DID NOT OPEN PROPERLY"
    common.wait_page_element_load(ADAPTER_WORKSHEET_PAGE.driver, ADAPTER_WORKSHEET_PAGE.worksheet_answers_textarea)
    assert len(ADAPTER_WORKSHEET_PAGE.get_worksheet_questions()) > 0, "QUESTIONS DID NOT LOAD PROPERLY"
    if len(WORKSHEET_QUESTIONS) > 0:
        for question in WORKSHEET_QUESTIONS:
            assert ADAPTER_WORKSHEET_PAGE.get_worksheet_answers_textarea().text == WORKSHEET_QUESTIONS.get(question), \
                "WORKSHEET ANSWERS WERE NOT SAVED!"
            common.LOGGER.info(agent=common_steps.get_agent_for_logs(),
                               message=f"worksheet answer for question '{question}' "
                                       f"found: '{ADAPTER_WORKSHEET_PAGE.get_worksheet_answers_textarea().text}'")
            if ADAPTER_WORKSHEET_PAGE.get_worksheet_next_button().is_enabled():
                ADAPTER_WORKSHEET_PAGE.get_worksheet_next_button().click()
            common.system_wait(1)
        # reset questions after the validation. avoid false positive if a new call is done.
        WORKSHEET_QUESTIONS = {}
        common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="worksheet questions reset")


@when("I fill the adapter worksheet")
def fill_adt_worksheet():
    # set questions
    for question_ in ADAPTER_WORKSHEET_PAGE.get_worksheet_questions():
        WORKSHEET_QUESTIONS[question_.text.strip()] = ''
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"worksheet questions set: {WORKSHEET_QUESTIONS}")

    # answer questions
    has_next_question = ADAPTER_WORKSHEET_PAGE.get_worksheet_next_button().is_enabled()
    while has_next_question:
        current_question_ = ADAPTER_WORKSHEET_PAGE.get_worksheet_current_question().text.strip()
        answer_ = f'question "{current_question_}" answer!'
        ADAPTER_WORKSHEET_PAGE.get_worksheet_answers_textarea().send_keys(answer_)
        WORKSHEET_QUESTIONS[current_question_] = answer_
        has_next_question = ADAPTER_WORKSHEET_PAGE.get_worksheet_next_button().is_enabled()
        if has_next_question:
            ADAPTER_WORKSHEET_PAGE.get_worksheet_next_button().click()
            common.system_wait(1)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"worksheet answers set: {WORKSHEET_QUESTIONS}")
    ADAPTER_WORKSHEET_PAGE.get_worksheet_finish_button().click()
    # TODO: check this behaviour
    common_steps.update_number_of_tabs(ADAPTER_WORKSHEET_PAGE.driver)
    common.switch_tabs(ADAPTER_WORKSHEET_PAGE.driver, tab_id=ADAPTER_WORKSHEET_PAGE.driver.window_handles[0])
