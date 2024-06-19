import common
from page_objects.login_page import LoginPage
from pytest_bdd import given, then, when
from test.initialization import base_setup
from step_definitions import home_page_steps, agent_steps, common_steps, chat_interaction_steps

LOGIN_PAGE = LoginPage()


@given("I am in login page")
@when("I am in login page")
def see_login_page():
    LOGIN_PAGE.open_page()
    common.wait_page_element_load(LOGIN_PAGE.driver, LOGIN_PAGE.login_button)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"login page loaded | url: {LOGIN_PAGE.url}")


@when("I am in direct login page")
def see_direct_login_page():
    LOGIN_PAGE.url = base_setup.LAB_CONFIGURATION.get('direct_login_url')
    see_login_page()


@when("I perform login")
def perform_login():
    agent = common_steps.get_free_agent()
    LOGIN_PAGE.get_user_input().send_keys(agent.get('user'))
    LOGIN_PAGE.get_password_input().send_keys(agent.get('pass'))
    LOGIN_PAGE.get_login_button().click()
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"login performed | user: {agent.get('user')} pass: {agent.get('pass')}")


@then("I perform logout")
def perform_logout():
    # get logged agents
    for agent_ in common_steps.AGENT_CREDENTIALS:
        agent_info = common_steps.AGENT_CREDENTIALS.get(agent_)
        if not agent_info.get('free') and agent_info.get('free') is not None:
            common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"logged agent found | agent info: {agent_info}")
            common_steps.set_current_browser(common.get_driver_by_instance(agent_info.get('driver'), False).get('instance'))
            common.switch_tabs(agent_steps.AGENT_HOME.driver, tab_title='Agent Desktop Plus')
            if common_steps.TEARDOWN:
                try:
                    if agent_steps.AGENT_HOME.get_set_disposition_button().is_displayed():
                        if agent_steps.AGENT_HOME.get_set_disposition_button().is_enabled():
                            agent_steps.set_disposition('No Disposition')
                            common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="active interaction disposed")
                except Exception as e:
                    common.LOGGER.debug(agent=common_steps.get_agent_for_logs(), message=f"an active interaction was found but some error occurred while trying to dispose it")
                    common.LOGGER.error(agent=common_steps.get_agent_for_logs(), message=f"{e,}")
                try:
                    if chat_interaction_steps.CHAT_INTERACTION_PAGE.get_set_disposition_button().is_displayed():
                        if chat_interaction_steps.CHAT_INTERACTION_PAGE.get_set_disposition_button().is_enabled():
                            chat_interaction_steps.dispose_chat()
                except Exception as e:
                    common.LOGGER.debug(agent=common_steps.get_agent_for_logs(), message="error when trying to dispose chat interaction. maybe the logout will not be correctly performed")
                    common.LOGGER.error(agent=common_steps.get_agent_for_logs(), message=f"{e,}")
            agent_steps.AGENT_HOME.get_agent_profile_button().click()
            agent_steps.AGENT_HOME.get_agent_logout_element().click()
            common.wait_page_element_load(agent_steps.AGENT_HOME.driver, agent_steps.AGENT_HOME.logout_reason_dialog)
            agent_steps.AGENT_HOME.get_confirm_logout_button().click()
            common.wait_page_to_be(agent_steps.AGENT_HOME.driver, 'index.html?loginError=true')
            common.wait_page_element_load(LOGIN_PAGE.driver, LOGIN_PAGE.user_input)
            common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"adp application logout success | current url: {LOGIN_PAGE.driver.current_url}")
            if agent_info.get('login_type') == 'emulation':
                tab_title_ = 'Five9 Inc. :: Applications' \
                    if common.TEST_INFO.get('lab') == 'qa02' else 'Five9. Inc. :: Applications'
                common.switch_tabs(driver_=agent_steps.AGENT_HOME.driver, tab_title=tab_title_)
                home_page_steps.HOME_PAGE.get_logout_element().click()
                common.wait_page_to_be(LOGIN_PAGE.driver, LOGIN_PAGE.url)
                common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"emulation logout success | current url: {LOGIN_PAGE.driver.current_url}")
            # release agent
            common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"releasing agent: {agent_}")
            agent_info['free'] = True
            agent_info['driver'] = None
            agent_info['login_type'] = None
            common_steps.AGENT_CREDENTIALS[agent_] = agent_info
            common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"agent released | agent info: {agent_info}")


@when("I see the home page")
def see_home_page():
    common.wait_element_to_be_clickable(home_page_steps.HOME_PAGE.driver, home_page_steps.HOME_PAGE.agent_span)
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"home page loaded | url: {home_page_steps.HOME_PAGE.url}")
