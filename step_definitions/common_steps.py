from selenium.common import NoSuchElementException

import common
import driver
from selenium.webdriver.common.by import By
from page_objects.common_page import CommonPage
from pytest_bdd import given, when, parsers
from step_definitions import login_steps

STARTED_PAGES = []
COMMON_PAGE = CommonPage()
MODAL_TYPES = {
    'skills': 'SELECT YOUR SKILLS',
    'station': 'STATION SETUP',
    'station_check': 'STATION CHECK',
    'inbound': '(Inbound)',
    'manual': '(Manual)'
}
AGENT_CREDENTIALS = {}


def reset_variables():
    """
    reset all variables to avoid missmatch use when run more than 1 test at once
    """
    pass


def update_number_of_tabs(driver_):
    common.system_wait(3)
    driver.DRIVERS.get(common.get_driver_by_instance(driver_))['number_of_tabs'] = len(driver_.window_handles)


def get_agent_by_driver(driver_):
    for agent_ in AGENT_CREDENTIALS:
        if AGENT_CREDENTIALS.get(agent_).get('driver') == driver_:
            return AGENT_CREDENTIALS.get(agent_)


def get_free_agent(login_type=None):
    agent = {}
    for agent_ in AGENT_CREDENTIALS:
        is_free = AGENT_CREDENTIALS.get(agent_).get('free')
        if is_free or is_free is None:
            agent = AGENT_CREDENTIALS.get(agent_)
            agent['free'] = False
            agent['driver'] = login_steps.LOGIN_PAGE.driver
            if not login_type:
                if 'qalogin' in login_steps.LOGIN_PAGE.url:
                    login_type = 'emulation'
                elif 'qaapp' in login_steps.LOGIN_PAGE.url:
                    login_type = 'direct'
                else:
                    login_type = 'unknown'
            agent['login_type'] = login_type
            AGENT_CREDENTIALS[agent_] = agent
            break
    if not agent:
        raise Exception('no free agent available')
    return agent


def _wait_modal_dialog(modal_type, timeout_in_seconds=15, open_=True):
    if open_:
        if modal_type == 'station':
            timeout_in_seconds = 300
        common.wait_page_element_load(driver_=COMMON_PAGE.driver,
                                      element_xpath=COMMON_PAGE.modal_dialog.replace('<title>',
                                                                                     MODAL_TYPES.get(modal_type)),
                                      timeout_in_seconds=timeout_in_seconds)
    for sec_ in range(timeout_in_seconds):
        if open_:
            modal = COMMON_PAGE.get_modal_dialog(title=MODAL_TYPES.get(modal_type))
            if modal.is_displayed():
                if MODAL_TYPES.get(modal_type).lower() in modal.text.lower():
                    return True
        else:
            if len(COMMON_PAGE.driver.find_elements(By.XPATH, COMMON_PAGE.modal_dialog)) == 0:
                return True
        common.system_wait(1)
    message = "open" if open_ else "close"
    raise TimeoutError(f'modal {MODAL_TYPES.get(modal_type)} was not {message} in {timeout_in_seconds} second(s).')


def wait_modal_dialog_close(modal_type, timeout_in_seconds=15):
    _wait_modal_dialog(modal_type=modal_type, timeout_in_seconds=timeout_in_seconds, open_=False)


def wait_modal_dialog_open(modal_type, timeout_in_seconds=15):
    _wait_modal_dialog(modal_type=modal_type, timeout_in_seconds=timeout_in_seconds)


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


def select_modal_next_button():
    button_clicked = False
    for time_ in range(10):  # 20s timeout
        common.system_wait(2)
        n_buttons = COMMON_PAGE.driver.find_elements(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Next'))
        o_buttons = COMMON_PAGE.driver.find_elements(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'OK'))
        y_buttons = COMMON_PAGE.driver.find_elements(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Yes'))
        v_buttons = COMMON_PAGE.driver.find_elements(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'View My Dashboard'))
        c_buttons = COMMON_PAGE.driver.find_elements(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Confirm'))
        if len(n_buttons) > 0 or len(o_buttons) > 0 or len(y_buttons) > 0 or len(v_buttons) > 0 or len(c_buttons) > 0:
            try:
                if COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Next')).is_displayed() \
                        and COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Next')).is_enabled:
                    COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Next')).click()
                    button_clicked = True
                    break
            except NoSuchElementException:
                pass
            try:
                if COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Next')).is_displayed() \
                        and COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Next')).is_enabled():
                    COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Next')).click()
                    button_clicked = True
                    break
            except NoSuchElementException:
                pass
            try:
                if COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'OK')).is_displayed() \
                        and COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'OK')).is_enabled():
                    COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'OK')).click()
                    button_clicked = True
                    break
            except NoSuchElementException:
                pass
            try:
                if COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Yes')).is_displayed() \
                        and COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Yes')).is_enabled():
                    COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Yes')).click()
                    button_clicked = True
                    break
            except NoSuchElementException:
                pass
            try:
                if COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'View My Dashboard')).is_displayed() \
                        and COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'View My Dashboard')).is_enabled():
                    COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'View My Dashboard')).click()
                    button_clicked = True
                    break
            except NoSuchElementException:
                pass
            try:
                if COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Confirm')).is_displayed() \
                        and COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Confirm')).is_enabled:
                    COMMON_PAGE.driver.find_element(By.XPATH, COMMON_PAGE.modal_submit_button.replace('<text>', 'Confirm')).click()
                    button_clicked = True
                    break
            except NoSuchElementException:
                pass
    common.system_wait(1)
    assert button_clicked, "COULD NOT FIND OR CLICK IN NEXT BUTTON"


@when("I check the new browser tab opened")
def check_new_tab():
    common.system_wait(5)
    driver_number_of_tabs = driver.DRIVERS.get(common.get_driver_by_instance(COMMON_PAGE.driver)).get('number_of_tabs')
    current_number_of_tabs = len(COMMON_PAGE.driver.window_handles)
    assert driver_number_of_tabs < current_number_of_tabs, \
        f"NEW TAB NOT FOUND. CURRENT NUMBER OF TABS: {current_number_of_tabs} SHOULD BE MORE THAN: {driver_number_of_tabs}"
    driver.DRIVERS.get(common.get_driver_by_instance(COMMON_PAGE.driver))['number_of_tabs'] = len(COMMON_PAGE.driver.window_handles)
    common.switch_tabs(driver_=COMMON_PAGE.driver, tab_id=COMMON_PAGE.driver.window_handles[
        driver.DRIVERS.get(common.get_driver_by_instance(COMMON_PAGE.driver)).get('number_of_tabs')-1])


@when("I close the current browser tab")
def close_current_browser_tab():
    common.BROWSER_TABS.pop(COMMON_PAGE.driver.current_window_handle)
    COMMON_PAGE.driver.close()
    common.system_wait(3)
    assert driver.DRIVERS.get(common.get_driver_by_instance(COMMON_PAGE.driver)).get('number_of_tabs') > len(COMMON_PAGE.driver.window_handles), \
        f"CURRENT TAB WAS NOT SUCCESSFULLY CLOSED: {COMMON_PAGE.driver.title}"
    driver.DRIVERS.get(common.get_driver_by_instance(COMMON_PAGE.driver))['number_of_tabs'] = len(COMMON_PAGE.driver.window_handles)
    common.switch_tabs(COMMON_PAGE.driver, tab_id=COMMON_PAGE.driver.window_handles[0])


@when(parsers.parse("I proceed to {step} step"))
def proceed_to_step(step):
    if step == 'next':
        select_modal_next_button()
    elif step == 'previous':
        COMMON_PAGE.get_modal_back_button().click()
    else:
        raise Exception('wrong step option. select "next" or "previous".')


@when(parsers.parse("I {action} the {skill_} skill"))
@when(parsers.parse("I {action} {skill_} skills"))
def select_skill(action, skill_):
    wait_modal_dialog_open('skills', 30)
    if skill_ == 'all':
        all_skills(action)
    else:
        _skill(skill_, action)


@when(parsers.parse("I set the browser number {browser}"))
@given(parsers.parse("I set the browser number {browser}"))
def set_current_browser(browser):
    if 'WebDriver' in str(type(browser)):
        driver_ = browser
    else:
        driver_ = driver.DRIVERS.get(str(int(browser) - 1)).get('instance')
    for page in STARTED_PAGES:
        page.driver = driver_
    common.switch_tabs(driver_=driver_, tab_id=driver_.current_window_handle)


@when(parsers.parse("I open a new tab in {url} url"))
def open_new_tab(url):
    if url == 'blank':
        COMMON_PAGE.driver.execute_script("window.open('about:blank');")
    else:
        COMMON_PAGE.driver.get(url)


@when(parsers.parse("I switch to tab with {title} title"))
def switch_to_tab_with_title(title):
    common.switch_tabs(COMMON_PAGE.driver, tab_title=title)
