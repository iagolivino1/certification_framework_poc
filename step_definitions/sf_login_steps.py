import common
from page_objects.sf_login_page import SFLoginPage
from pytest_bdd import given, then, when
from step_definitions import sf_home_page_steps, agent_steps, common_steps

LOGIN_PAGE = SFLoginPage()
AGENT_CREDENTIALS = {}

@given("I am in SF login page")
@when("I am in SF login page")
def see_sf_login_page():
    LOGIN_PAGE.open_page()
    common.wait_page_element_load(LOGIN_PAGE.driver, LOGIN_PAGE.login_button)

@when("I perform SF login")
def perform_login():
    agent = AGENT_CREDENTIALS.get('agent_0')
    LOGIN_PAGE.get_user_input().send_keys(agent.get('user'))
    LOGIN_PAGE.get_password_input().send_keys(agent.get('pass'))
    LOGIN_PAGE.get_login_button().click()

@when("I see the SF home page")
def see_home_page():
    common.wait_element_to_be_clickable(sf_home_page_steps.HOME_PAGE.driver, sf_home_page_steps.HOME_PAGE.logo_img)