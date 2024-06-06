from pytest_bdd import when
from selenium.webdriver import Keys

import common
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


@when("I perform login in adapter")
def perform_adapter_login():
    agent = common_steps.get_free_agent(login_type='adapter')
    ADAPTER_LOGIN_PAGE.get_adapter_user_input().send_keys(agent.get('user'))
    ADAPTER_LOGIN_PAGE.get_adapter_password_input().send_keys(agent.get('pass'))
    ADAPTER_LOGIN_PAGE.get_adapter_login_button().click()


@when("I am in adapter login page")
def see_adt_login_page():
    assert ADAPTER_LOGIN_PAGE.url in ADAPTER_LOGIN_PAGE.driver.current_url
    common.wait_page_element_load(ADAPTER_LOGIN_PAGE.driver, ADAPTER_LOGIN_PAGE.adapter_user_input)


@when("I perform logout in adapter")
def adapter_logout():
    # get logged agents
    for agent_ in common_steps.AGENT_CREDENTIALS:
        agent_info = common_steps.AGENT_CREDENTIALS.get(agent_)
        if not agent_info.get('free') and agent_info.get('free') is not None:
            if agent_info.get('login_type') == 'adapter':
                common_steps.set_current_browser(common.get_driver_by_instance(agent_info.get('driver'), False).get('instance'))
                common.switch_tabs(common_steps.COMMON_PAGE.driver, tab_title='Adapter')
                common.wait_element_to_be_clickable(common_steps.COMMON_PAGE.driver, adapter_steps.ADAPTER_PAGE.agent_state_button)
                adapter_steps.ADAPTER_PAGE.get_agent_state_button().click()
                common.wait_element_to_be_clickable(common_steps.COMMON_PAGE.driver, adapter_steps.ADAPTER_PAGE.logout_button)
                adapter_steps.ADAPTER_PAGE.get_logout_button().click()
                common.wait_page_to_be(common_steps.COMMON_PAGE.driver, ADAPTER_LOGIN_PAGE.url)

                # release agent
                agent_info['free'] = True
                agent_info['driver'] = None
                agent_info['login_type'] = None
                common_steps.AGENT_CREDENTIALS[agent_] = agent_info
