from pytest_bdd import when, then
from selenium.webdriver import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

import common
import pyautogui
import driver
from page_objects.adapters.adapter_login_page import AdapterLoginPage
from step_definitions import common_steps
from step_definitions.adapters import adapter_steps

ADAPTER_LOGIN_PAGE = AdapterLoginPage()
PLATFORM_HOTKEYS = {
    'windows': [Keys.CONTROL, 'ctrl'],
    'mac': [Keys.COMMAND, 'command'],
    'linux': [Keys.CONTROL, 'control']
}
EXTENSION_NAME = "Five9 Agent Desktop Toolkit"

def check_force_login(agent):
    try:
        common.wait_element_to_be_clickable(ADAPTER_LOGIN_PAGE.driver,ADAPTER_LOGIN_PAGE.force_login_button,5)
        ADAPTER_LOGIN_PAGE.get_force_login_button().click()
        return
    except (NoSuchElementException, TimeoutException):
        return


@when("I perform login in adapter")
def perform_adapter_login():
    agent = common_steps.get_free_agent(login_type='adapter')
    ADAPTER_LOGIN_PAGE.get_adapter_user_input().send_keys(agent.get('user'))
    ADAPTER_LOGIN_PAGE.get_adapter_password_input().send_keys(agent.get('pass'))
    ADAPTER_LOGIN_PAGE.get_adapter_login_button().click()
    check_force_login(agent) #Used on SF - should not break other tests


@when("I am in adapter login page")
def see_adt_login_page():
    assert ADAPTER_LOGIN_PAGE.url in ADAPTER_LOGIN_PAGE.driver.current_url
    common.wait_page_element_load(ADAPTER_LOGIN_PAGE.driver, ADAPTER_LOGIN_PAGE.adapter_user_input)


@when("I perform logout in adapter")
@then("I perform logout in adapter")
def adapter_logout():
    # get logged agents
    for agent_ in common_steps.AGENT_CREDENTIALS:
        agent_info = common_steps.AGENT_CREDENTIALS.get(agent_)
        if not agent_info.get('free') and agent_info.get('free') is not None:
            if agent_info.get('login_type') == 'adapter':
                common_steps.set_current_browser(common.get_driver_by_instance(agent_info.get('driver'), False).get('instance'))
                if common_steps.COMMON_PAGE.driver.title.__contains__("Salesforce"):
                    common.find_and_switch_to_frame(common_steps.COMMON_PAGE.driver,"SoftphoneIframe")
                else:
                    common.switch_tabs(common_steps.COMMON_PAGE.driver, tab_title='Adapter')
                common.wait_element_to_be_clickable(common_steps.COMMON_PAGE.driver, adapter_steps.ADAPTER_PAGE.agent_state_button)
                adapter_steps.ADAPTER_PAGE.get_agent_state_button().click()
                common.wait_element_to_be_clickable(common_steps.COMMON_PAGE.driver, adapter_steps.ADAPTER_PAGE.logout_button)
                adapter_steps.ADAPTER_PAGE.get_logout_button().click()
                if not common_steps.COMMON_PAGE.driver.title.__contains__("Salesforce"):
                    common.wait_page_to_be(common_steps.COMMON_PAGE.driver, ADAPTER_LOGIN_PAGE.url)

                # release agent
                agent_info['free'] = True
                agent_info['driver'] = None
                agent_info['login_type'] = None
                common_steps.AGENT_CREDENTIALS[agent_] = agent_info

@when("I launch the adapter")
def launch_adapter():
    # open the adapter window
    for _driver in driver.DRIVERS:
        driver_ = driver.DRIVERS.get(_driver).get('instance')
        driver_.switch_to.window(driver_.current_window_handle)
        for attempt in range(10):
            common.wait_element_to_be_clickable(driver_, "//body")
            common.click_element(driver_, driver_.find_element(By.TAG_NAME, "body"))
            pyautogui.hotkey(
                PLATFORM_HOTKEYS.get(driver_.caps.get('platformName'))[1], 'i')
            common.system_wait(2)
            if len(driver_.window_handles) > 1:
                common.switch_tabs(driver_=driver_, tab_id=driver_.window_handles[1])
                if driver_.title != 'Adapter':
                    common.wait_page_element_load(driver_, "//*[@id='username']", 60)
                    break