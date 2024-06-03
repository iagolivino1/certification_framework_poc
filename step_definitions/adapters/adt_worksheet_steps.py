import common
from pytest_bdd import when
from page_objects.adapters.adt_worksheet_page import ADTWorksheetPage
from step_definitions import common_steps

ADT_WORKSHEET_PAGE = ADTWorksheetPage()
WORKSHEET_QUESTIONS = {}


@when("I check the call worksheet window")
def check_worksheet_window():
    assert 'Five9 Adapter - Worksheet' in ADT_WORKSHEET_PAGE.driver.title, "WORKSHEET WINDOW DID NOT OPEN PROPERLY"
    common.wait_page_element_load(ADT_WORKSHEET_PAGE.driver, ADT_WORKSHEET_PAGE.worksheet_answers_textarea)
    assert len(ADT_WORKSHEET_PAGE.get_worksheet_questions()) > 0, "QUESTIONS DID NOT LOAD PROPERLY"
    if len(WORKSHEET_QUESTIONS) > 0:
        for question in WORKSHEET_QUESTIONS:
            assert ADT_WORKSHEET_PAGE.get_worksheet_answers_textarea().text == WORKSHEET_QUESTIONS.get(question), \
                "WORKSHEET ANSWERS WERE NOT SAVED!"
            if ADT_WORKSHEET_PAGE.get_worksheet_next_button().is_enabled():
                ADT_WORKSHEET_PAGE.get_worksheet_next_button().click()
            common.system_wait(1)


@when("I fill the adt worksheet")
def fill_adt_worksheet():
    # set questions
    for question_ in ADT_WORKSHEET_PAGE.get_worksheet_questions():
        WORKSHEET_QUESTIONS[question_.text.strip()] = ''

    # answer questions
    has_next_question = ADT_WORKSHEET_PAGE.get_worksheet_next_button().is_enabled()
    while has_next_question:
        current_question_ = ADT_WORKSHEET_PAGE.get_worksheet_current_question().text.strip()
        answer_ = f'question "{current_question_}" answer!'
        ADT_WORKSHEET_PAGE.get_worksheet_answers_textarea().send_keys(answer_)
        WORKSHEET_QUESTIONS[current_question_] = answer_
        has_next_question = ADT_WORKSHEET_PAGE.get_worksheet_next_button().is_enabled()
        if has_next_question:
            ADT_WORKSHEET_PAGE.get_worksheet_next_button().click()
            common.system_wait(1)
    ADT_WORKSHEET_PAGE.get_worksheet_finish_button().click()
    # TODO: check this behaviour
    common_steps.update_number_of_tabs(ADT_WORKSHEET_PAGE.driver)
