import common
from page_objects.sf_login_page import SFLoginPage
from page_objects.sf_agent_home_page import SFAgentHomePage
from pytest_bdd import given, when

LOGIN_PAGE = SFLoginPage()
HOME_PAGE = SFAgentHomePage()
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
    common.wait_element_to_be_clickable(HOME_PAGE.driver, HOME_PAGE.logo_img)