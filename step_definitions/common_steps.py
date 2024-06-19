import common
import driver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from page_objects.common_page import CommonPage
from pytest_bdd import given, when, parsers
from step_definitions import login_steps
from selenium.webdriver import Keys

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
PLATFORM_HOTKEYS = {
    'windows': [Keys.CONTROL, 'ctrl'],
    'mac': [Keys.COMMAND, 'command'],
    'linux': [Keys.CONTROL, 'control']
}
TEARDOWN = False


def reset_variables():
    """
    reset all variables to avoid missmatch use when run more than 1 test at once
    """
    global TEARDOWN
    TEARDOWN = True
    pass


def update_number_of_tabs(driver_):
    common.system_wait(3)
    driver.DRIVERS.get(common.get_driver_by_instance(driver_))['number_of_tabs'] = len(driver_.window_handles)


def get_agent_by_driver(driver_):
    for agent_ in AGENT_CREDENTIALS:
        if AGENT_CREDENTIALS.get(agent_).get('driver') == driver_:
            return AGENT_CREDENTIALS.get(agent_)


def get_agent_by_attributes(user=None, station_id=None, inbound_camp=None, outbound_camp=None, chat_camp=None, ready_for=None):
    agent = {}
    for agent_ in AGENT_CREDENTIALS:
        tmp_agent = AGENT_CREDENTIALS.get(agent_)
        try:
            if user:
                assert tmp_agent.get('user') == user
            if station_id:
                assert tmp_agent.get('station').get('station_id') == station_id
            if inbound_camp:
                assert tmp_agent.get('inbound_camp') == inbound_camp
            if outbound_camp:
                assert tmp_agent.get('outbound_camp') == outbound_camp
            if chat_camp:
                assert tmp_agent.get('chat_camp') == chat_camp
            if ready_for:
                assert ready_for in tmp_agent.get('ready_channels')
            agent = tmp_agent
        except AssertionError:
            continue
        except AttributeError:
            continue
    return agent


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


def set_adapter_shortcut(driver_, extension_text, return_id=False):
    driver_.get("chrome://extensions")
    extension_manager_element_shadow = driver_.find_element(By.XPATH, "//extensions-manager")
    extension_items_list_shadow = extension_manager_element_shadow.shadow_root.find_element(By.CSS_SELECTOR,
                                                                                            "#items-list")
    extensions = extension_items_list_shadow.shadow_root.find_elements(By.CSS_SELECTOR, "extensions-item")
    selected_extension = None
    for extension in extensions:
        extension_name = extension.shadow_root.find_element(By.CSS_SELECTOR, "#name").text.strip()
        if extension_name == extension_text:
            selected_extension = extension
            break
    if not selected_extension:
        raise Exception(f"extension {extension_text} not found")

    # open extension options
    selected_extension.shadow_root.find_element(By.CSS_SELECTOR, "#detailsButton").click()
    common.wait_page_to_be(driver_, "?id=")
    if return_id:
        return driver_.current_url.split("?id=")[1].strip()

    left_panel_shadow = extension_manager_element_shadow.shadow_root.find_element(By.CSS_SELECTOR, "extensions-sidebar")
    keyboard_shortcuts = left_panel_shadow.shadow_root.find_element(By.CSS_SELECTOR, "a#sectionsShortcuts")
    keyboard_shortcuts.click()

    keyboard_shortcuts_content_shadow = extension_manager_element_shadow.shadow_root.find_element(By.CSS_SELECTOR,
                                                                                                  "extensions-keyboard-shortcuts")
    extension_cards = keyboard_shortcuts_content_shadow.shadow_root.find_elements(By.CSS_SELECTOR, ".shortcut-card")
    selected_extension_card = None
    for extension_card in extension_cards:
        if extension_text in extension_card.text:
            selected_extension_card = extension_card
            break
    if not selected_extension_card:
        raise Exception(f"card for {extension_text} extension not found")

    action = ActionChains(driver_)
    edit_shortcut_shadow = selected_extension_card.find_element(By.CSS_SELECTOR, "extensions-shortcut-input")
    edit_shortcut_button = edit_shortcut_shadow.shadow_root.find_element(By.CSS_SELECTOR, "cr-icon-button#edit")
    edit_shortcut_button.click()
    edit_shortcut_shadow.shadow_root.find_element(By.CSS_SELECTOR, "cr-input").shadow_root.find_element(By.CSS_SELECTOR, "#input").click()
    action.key_down(PLATFORM_HOTKEYS.get(driver_.caps.get('platformName'))[0])\
        .send_keys('i')\
        .key_up(PLATFORM_HOTKEYS.get(driver_.caps.get('platformName'))[0])\
        .perform()
    
def set_adapter_url(driver_, extension_id, steps_obj, adpt_url='adapter_login_url'):
    lab_config = f"configuration/lab/{common.get_config_file_section('config.yml', 'configuration').get('lab')}.yml"
    adapter_url = common.get_config_file_section(lab_config, 'configuration').get(adpt_url)
    if not adapter_url:
        adapter_url = steps_obj.url
    steps_obj.url = adapter_url
    driver_.get(f"chrome-extension://{extension_id}/options.html")
    common.system_wait(2)

    # set extension url
    if adpt_url != 'adapter_login_url':
        driver_.find_element(By.XPATH, "//select[@id='domain-select']/option[@value='Custom']").click()
    input_url = driver_.find_element(By.XPATH, "//input[@id='url'] | //input[@id='custom-host']")
    input_url.clear()
    input_url.click()
    input_url.send_keys(adapter_url)
    try:
        assert input_url.get_attribute('value') == adapter_url
    except AssertionError:
        input_url.clear()
        input_url.send_keys(adapter_url)
        assert input_url.get_attribute('value') == adapter_url, "COULD NOT SET THE CORRECT URL"
    driver_.find_element(By.XPATH, "//button[@id='save']").click()
    common.wait_element_attribute_contains(driver_, "//mark[@id='status']", 'innerText', "Options Saved")
    tab_info = {'title': driver_.title,
                'browser_number': int(common.get_driver_by_instance(driver_))}
    common.BROWSER_TABS[driver_.current_window_handle] = tab_info


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
