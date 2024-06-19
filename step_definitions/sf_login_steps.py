import common
from page_objects.sf_login_page import SFLoginPage
from pytest_bdd import given, when
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from step_definitions import common_steps

LOGIN_PAGE = SFLoginPage()
AGENT_CREDENTIALS = {}


def check_additional_authentication():
    try:
        title = LOGIN_PAGE.get_ns_additional_auth_title().text
        if title == "Additional Authentication Required":
            LOGIN_PAGE.get_ns_additional_pass().send_keys("meet")
            LOGIN_PAGE.get_ns_additional_submit_btn().click()
        return
    except (NoSuchElementException, TimeoutException):
        return


@given("I am in SF login page")
@when("I am in SF login page")
@given("I am in NetSuite login page")
@when("I am in NetSuite login page")
def see_sf_login_page():
    LOGIN_PAGE.open_page()
    common.wait_page_element_load(LOGIN_PAGE.driver, LOGIN_PAGE.login_button)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"sf login page loaded | url: {LOGIN_PAGE.url}")


@when("I perform SF login")
@when("I perform NetSuite login")
def perform_login():
    agent = AGENT_CREDENTIALS.get('agent_0')
    LOGIN_PAGE.get_user_input().send_keys(agent.get('user'))
    LOGIN_PAGE.get_password_input().send_keys(agent.get('pass'))
    LOGIN_PAGE.get_login_button().click()
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"login performed | user: {agent.get('user')} pass: {agent.get('pass')}")


@when("I see the SF home page")
@when("I see the NetSuite home page")
def see_home_page():
    check_additional_authentication()
    common.wait_element_to_be_clickable(LOGIN_PAGE.driver, LOGIN_PAGE.logo_img)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"sf home page loaded: {LOGIN_PAGE.driver.current_url}")
