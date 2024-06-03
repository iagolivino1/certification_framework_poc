import common
from page_objects.login_page import LoginPage
from pytest_bdd import given, then, when
from step_definitions import home_page_steps, agent_steps, common_steps

LOGIN_PAGE = LoginPage()


@given("I am in login page")
@when("I am in login page")
def see_login_page():
    LOGIN_PAGE.open_page()
    common.wait_page_element_load(LOGIN_PAGE.driver, LOGIN_PAGE.login_button)


@when("I perform login")
def perform_login():
    agent = common_steps.get_free_agent()
    LOGIN_PAGE.get_user_input().send_keys(agent.get('user'))
    LOGIN_PAGE.get_password_input().send_keys(agent.get('pass'))
    LOGIN_PAGE.get_login_button().click()


@then("I perform logout")
def perform_logout():
    # get logged agents
    for agent_ in common_steps.AGENT_CREDENTIALS:
        agent_info = common_steps.AGENT_CREDENTIALS.get(agent_)
        if not agent_info.get('free') and agent_info.get('free') is not None:
            common_steps.set_current_browser(common.get_driver_by_instance(agent_info.get('driver'), False).get('instance'))
            common.switch_tabs(agent_steps.AGENT_HOME.driver, tab_title='Agent Desktop Plus')
            agent_steps.AGENT_HOME.get_agent_profile_button().click()
            agent_steps.AGENT_HOME.get_agent_logout_element().click()
            common.wait_page_element_load(agent_steps.AGENT_HOME.driver, agent_steps.AGENT_HOME.logout_reason_dialog)
            agent_steps.AGENT_HOME.get_confirm_logout_button().click()
            common.wait_page_to_be(agent_steps.AGENT_HOME.driver, 'index.html?loginError=true')
            if agent_info.get('login_type') == 'emulation':
                common.switch_tabs(driver_=agent_steps.AGENT_HOME.driver, tab_title='Five9. Inc. :: Applications')
                home_page_steps.HOME_PAGE.get_logout_element().click()
                common.wait_page_to_be(LOGIN_PAGE.driver, LOGIN_PAGE.url)
            # release agent
            agent_info['free'] = True
            agent_info['driver'] = None
            agent_info['login_type'] = None
            common_steps.AGENT_CREDENTIALS[agent_] = agent_info


@when("I see the home page")
def see_home_page():
    common.wait_element_to_be_clickable(home_page_steps.HOME_PAGE.driver, home_page_steps.HOME_PAGE.agent_span)
