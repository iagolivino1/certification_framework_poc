import common
from page_objects.agent_home_page import AgentHomePage
from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from pytest_bdd import (
    given,
    then,
    when
)

LOGIN_PAGE = None
AGENT_HOME = None
HOME_PAGE = None
CREDENTIALS = None


def set_pages(driver):
    # set all pages that will be used in the test
    global AGENT_HOME, HOME_PAGE, LOGIN_PAGE, CREDENTIALS
    AGENT_HOME = AgentHomePage(driver)
    HOME_PAGE = HomePage(driver)
    LOGIN_PAGE = LoginPage(driver)
    CREDENTIALS = common.get_config_file_section("config.ini", 'credentials')


@given("I am in login page")
def see_login_page(driver):
    set_pages(driver)
    LOGIN_PAGE.open_page()
    common.wait_page_element_load(driver, LOGIN_PAGE.login_button)


@when("I perform login")
def perform_login():
    LOGIN_PAGE.get_user_input().send_keys(CREDENTIALS.get('user'))
    LOGIN_PAGE.get_password_input().send_keys(CREDENTIALS.get('pass'))
    LOGIN_PAGE.get_login_button().click()


@then("I perform logout")
def perform_logout(driver):
    driver.switch_to.window(driver.current_window_handle)
    AGENT_HOME.get_agent_profile_button().click()
    AGENT_HOME.get_agent_logout_element().click()
    common.wait_page_element_load(driver, AGENT_HOME.logout_reason_dialog)
    AGENT_HOME.get_confirm_logout_button().click()
    common.wait_page_to_be(driver, 'https://app.eu.five9.com/index.html?loginError=true')
    common.switch_tabs(driver)
    HOME_PAGE.get_logout_element().click()
    common.wait_page_to_be(driver, LOGIN_PAGE.url)


@when("I see the home page")
def see_home_page(driver):
    common.wait_element_to_be_clickable(driver, HOME_PAGE.agent_span)
