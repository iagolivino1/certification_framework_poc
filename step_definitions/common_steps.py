import common
from selenium.webdriver.common.by import By

import driver
from page_objects.common_page import CommonPage
from pytest_bdd import given, when, parsers
from step_definitions import login_steps

STARTED_PAGES = []
COMMON_PAGE = CommonPage()
MODAL_TYPES = {
    'skills': 'SELECT YOUR SKILLS',
    'station': 'STATION SETUP',
    'station_check': 'STATION CHECK'
}


def reset_variables():
    """
    reset all variables to avoid missmatch use when run more than 1 test at once
    """
    pass


def get_free_agent():
    agent = {}
    for agent_ in login_steps.AGENT_CREDENTIALS:
        is_free = login_steps.AGENT_CREDENTIALS.get(agent_).get('free')
        if is_free or is_free is None:
            agent = login_steps.AGENT_CREDENTIALS.get(agent_)
            agent['free'] = False
            login_steps.AGENT_CREDENTIALS[agent_] = agent
            break
    if not agent:
        raise Exception('no free agent available')
    return agent


def wait_modal_dialog_open(modal_type, timeout_in_seconds=15):
    common.wait_page_element_load(driver=COMMON_PAGE.driver,
                                  element_xpath=COMMON_PAGE.modal_dialog.replace('<title>', MODAL_TYPES.get(modal_type)),
                                  timeout_in_seconds=300)
    common.wait_element_to_be_clickable(driver=COMMON_PAGE.driver,
                                        element_xpath=COMMON_PAGE.modal_submit_button)
    for sec_ in range(timeout_in_seconds):
        modal = COMMON_PAGE.get_modal_dialog(title=MODAL_TYPES.get(modal_type))
        if modal.is_displayed():
            if MODAL_TYPES.get(modal_type) in modal.text:
                return True
        common.system_wait(1)
    raise TimeoutError(f'modal {MODAL_TYPES.get(modal_type)} was not displayed in {timeout_in_seconds} second(s).')


def all_skills(action='select'):
    if action == 'select':
        if COMMON_PAGE.get_all_skills_button().text.strip() == 'Select All':
            COMMON_PAGE.get_all_skills_button().click()
            assert COMMON_PAGE.get_all_skills_button().text.strip() == 'De-Select All'
    else:
        if COMMON_PAGE.get_all_skills_button().text.strip() == 'De-Select All':
            COMMON_PAGE.get_all_skills_button().click()
        assert COMMON_PAGE.get_all_skills_button().text.strip() == 'Select All'


def _skill(skill, action='select'):
    validation_ = 'true'
    for skill_ in COMMON_PAGE.get_available_skills():
        if skill_.text == skill:
            if action == 'select':
                if skill.find_element(By.XPATH, "./i").get_attibute('aria-checked') == 'false':
                    skill_.click()
            else:
                if skill.find_element(By.XPATH, "./i").get_attibute('aria-checked') == 'true':
                    skill_.click()
                    validation_ = 'false'
            assert skill.find_element(By.XPATH, "./i").get_attibute('aria-checked') == validation_
            break


@when("I check the second browser tab opened")
def check_new_tab():
    common.switch_tabs(COMMON_PAGE.driver)


@when(parsers.parse("I proceed to {step} step"))
def proceed_to_step(step):
    if step == 'next':
        COMMON_PAGE.get_modal_submit_button().click()
    elif step == 'previous':
        COMMON_PAGE.get_modal_back_button().click()
    else:
        raise Exception('wrong step option. select "next" or "previous".')


@when(parsers.parse("I {action} the {skill_} skill"))
@when(parsers.parse("I {action} {skill_} skills"))
def select_skill(action, skill_):
    # check if some dialog will appear. in this case, the skills one
    wait_modal_dialog_open('skills', 30)
    if skill_ == 'all':
        all_skills(action)
    else:
        _skill(skill_, action)


@when(parsers.parse("I set the browser number {browser}"))
@given(parsers.parse("I set the browser number {browser}"))
def set_current_browser(browser):
    for page in STARTED_PAGES:
        page.driver = driver.DRIVERS[int(browser)-1]
