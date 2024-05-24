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
            agent['driver'] = login_steps.LOGIN_PAGE.driver
            if 'qalogin' in login_steps.LOGIN_PAGE.url:
                agent['login_type'] = 'emulation'
            elif 'qaapp' in login_steps.LOGIN_PAGE.url:
                agent['login_type'] = 'direct'
            else:
                agent['login_type'] = 'unknown'
            login_steps.AGENT_CREDENTIALS[agent_] = agent
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

def all_skills_sf(action='select'):
    common.wait_page_element_load(COMMON_PAGE.driver,COMMON_PAGE.modal_dialog_skills_sf.replace('<title>',
                                                                                     'Select Your Skills'))
    if action == 'select' and not COMMON_PAGE.get_all_skills_sf_checkbox().is_selected():
        COMMON_PAGE.get_all_skills_sf_label().click()
    elif action == 'select' and COMMON_PAGE.get_all_skills_sf_checkbox().is_selected():
        pass
    elif not action == 'select' and not COMMON_PAGE.get_all_skills_sf_checkbox().is_selected():
        pass
    else:
        COMMON_PAGE.get_all_skills_button().click()

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
    next_button_texts = ['Next', 'OK', 'Yes', 'View My Dashboard', 'Confirm']
    text_ = ''
    for text in next_button_texts:
        text_ = text
        try:
            if COMMON_PAGE.get_modal_submit_button(text).is_displayed():
                common.system_wait(1)
                common.wait_element_to_be_clickable(COMMON_PAGE.driver, COMMON_PAGE.modal_submit_button.replace('<text>', text))
                COMMON_PAGE.get_modal_submit_button(text).click()
                return True
        except Exception as e:
            print(e)
        common.system_wait(0.5)
    raise Exception(f"NOT POSSIBLE TO FIND AND CLICK ON {text_} BUTTON!")


@when("I check the new browser tab opened")
def check_new_tab():
    driver.DRIVERS.get(common.get_driver_by_instance(COMMON_PAGE.driver))['number_of_tabs'] = len(COMMON_PAGE.driver.window_handles)
    common.switch_tabs(driver_=COMMON_PAGE.driver, tab_id=COMMON_PAGE.driver.window_handles[
        driver.DRIVERS.get(common.get_driver_by_instance(COMMON_PAGE.driver)).get('number_of_tabs')-1])


@when("I close the current browser tab")
def close_current_browser_tab():
    common.BROWSER_TABS.pop(COMMON_PAGE.driver.current_window_handle)
    COMMON_PAGE.driver.close()
    assert driver.DRIVERS.get(common.get_driver_by_instance(COMMON_PAGE.driver)).get('number_of_tabs') > len(COMMON_PAGE.driver.window_handles), \
        f"CURRENT TAB WAS NOT SUCCESSFULLY CLOSED: {COMMON_PAGE.driver.title}"
    driver.DRIVERS.get(common.get_driver_by_instance(COMMON_PAGE.driver))['number_of_tabs'] = len(COMMON_PAGE.driver.window_handles)
    common.switch_tabs(COMMON_PAGE.driver, tab_id=COMMON_PAGE.driver.window_handles[len(COMMON_PAGE.driver.window_handles)-1])
    # log success


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
    # check if some dialog will appear. in this case, the skills one
    wait_modal_dialog_open('skills', 30)
    if skill_ == 'all':
        all_skills(action)
    else:
        _skill(skill_, action)


@when(parsers.parse("I {action} the {skill_} skill on SF"))
@when(parsers.parse("I {action} {skill_} skills on SF"))
def select_skill(action, skill_):
    if skill_ == 'all':
        all_skills_sf(action)
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


@when(parsers.parse("I open a new tab in {url} url"))
def open_new_tab(url):
    if url == 'blank':
        COMMON_PAGE.driver.execute_script("window.open('about:blank');")
    else:
        COMMON_PAGE.driver.get(url)