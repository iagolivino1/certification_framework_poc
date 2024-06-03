from pytest_bdd import when
from selenium.webdriver import Keys

import common
from page_objects.adapters.adt_login_page import ADTLoginPage
from step_definitions import common_steps
from step_definitions.adapters import adt_adapter_steps

ADT_LOGIN_PAGE = ADTLoginPage()
PLATFORM_HOTKEYS = {
    'windows': [Keys.CONTROL, 'ctrl'],
    'mac': [Keys.COMMAND, 'command'],
    'linux': [Keys.CONTROL, 'control']
}
EXTENSION_NAME = "Five9 Agent Desktop Toolkit"


@when("I perform login in adapter")
def perform_adapter_login():
    agent = common_steps.get_free_agent(login_type='adapter')
    ADT_LOGIN_PAGE.get_adapter_user_input().send_keys(agent.get('user'))
    ADT_LOGIN_PAGE.get_adapter_password_input().send_keys(agent.get('pass'))
    ADT_LOGIN_PAGE.get_adapter_login_button().click()


@when("I am in adt login page")
def see_adt_login_page():
    assert ADT_LOGIN_PAGE.url in ADT_LOGIN_PAGE.driver.current_url


@when("I perform logout in adapter")
def adapter_logout():
    # get logged agents
    for agent_ in common_steps.AGENT_CREDENTIALS:
        agent_info = common_steps.AGENT_CREDENTIALS.get(agent_)
        if not agent_info.get('free') and agent_info.get('free') is not None:
            if agent_info.get('login_type') == 'adapter':
                common_steps.set_current_browser(common.get_driver_by_instance(agent_info.get('driver'), False).get('instance'))
                common.switch_tabs(common_steps.COMMON_PAGE.driver, tab_title='Adapter')
                adt_adapter_steps.open_adapter_dispositions()
                common.wait_element_to_be_clickable(common_steps.COMMON_PAGE.driver, adt_adapter_steps.ADT_ADAPTER_PAGE.logout_button)
                adt_adapter_steps.ADT_ADAPTER_PAGE.get_logout_button().click()
                common.wait_page_element_load(common_steps.COMMON_PAGE.driver, ADT_LOGIN_PAGE.adapter_user_input)

                # release agent
                agent_info['free'] = True
                agent_info['driver'] = None
                agent_info['login_type'] = None
                common_steps.AGENT_CREDENTIALS[agent_] = agent_info
