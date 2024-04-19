import common
from page_objects.login_page import LoginPage
from pytest_bdd import given, then, when
from step_definitions import home_page_steps, agent_steps, common_steps

LOGIN_PAGE = LoginPage()
AGENT_CREDENTIALS = {}


@given("I am in login page")
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
    agent_steps.AGENT_HOME.driver.switch_to.window(agent_steps.AGENT_HOME.driver.current_window_handle)
    agent_steps.AGENT_HOME.get_agent_profile_button().click()
    agent_steps.AGENT_HOME.get_agent_logout_element().click()
    common.wait_page_element_load(agent_steps.AGENT_HOME.driver, agent_steps.AGENT_HOME.logout_reason_dialog)
    agent_steps.AGENT_HOME.get_confirm_logout_button().click()
    common.wait_page_to_be(agent_steps.AGENT_HOME.driver, 'index.html?loginError=true')
    common.switch_tabs(agent_steps.AGENT_HOME.driver)
    home_page_steps.HOME_PAGE.get_logout_element().click()
    common.wait_page_to_be(LOGIN_PAGE.driver, LOGIN_PAGE.url)


@when("I see the home page")
def see_home_page():
    common.wait_element_to_be_clickable(home_page_steps.HOME_PAGE.driver, home_page_steps.HOME_PAGE.agent_span)
