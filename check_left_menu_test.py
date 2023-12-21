# It is the same scenario as bdd. Only scripting without any test framework
import common
from page_objects.agent_home_page import AgentHomePage
from driver import Driver
from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.station_setup_page import StationSetupPage


def main():
    url = "https://ondemand.eu-central-1.saucelabs.com:443/wd/hub"
    driver = Driver(url).driver

    try:
        login_ = LoginPage(driver)
        login_.open_page()
        login_.get_user_input().send_keys('<five9_user>')
        login_.get_password_input().send_keys('<five9_pass>')
        login_.get_login_button().click()

        home_ = HomePage(driver)
        common.wait_page_element_load(driver, home_.agent_span)
        home_.get_agent_span().click()
        home_.get_web_agent_item().click()

        # should open a new tab with ADP -> switch to the new tab
        station_setup_ = StationSetupPage(driver)
        common.switch_tabs(driver)
        common.wait_page_element_load(driver, station_setup_.none_station, 120)
        station_setup_.get_none_station_type().click()
        station_setup_.get_next_button().click()

        agent_home_ = AgentHomePage(driver)
        common.wait_page_element_load(driver, agent_home_.agent_activity_button, timeout_in_seconds=60)

        # assert the elements visibility on page...
        common.assert_condition(agent_home_.get_agent_status_button().is_displayed(), "STATUS BUTTON IS NOT VISIBLE")
        common.assert_condition(agent_home_.get_agent_home_button().is_displayed(), "HOME BUTTON IS NOT VISIBLE")
        common.assert_condition(agent_home_.get_agent_voice_button().is_displayed(), "CALL BUTTON IS NOT VISIBLE")
        common.assert_condition(agent_home_.get_agent_voicemail_button().is_displayed(), "VOICEMAIL BUTTON IS NOT VISIBLE")

        # logout user
        agent_home_.get_agent_profile_button().click()
        agent_home_.get_agent_logout_element().click()
        common.wait_page_element_load(driver, agent_home_.logout_reason_dialog)
        agent_home_.get_confirm_logout_button().click()
        common.wait_page_to_be(driver, 'https://app.eu.five9.com/index.html?loginError=true')

        # switch back to env home page
        common.switch_tabs(driver)
        home_.get_logout_element().click()
        common.wait_page_to_be(driver, login_.url)
    except Exception as e:
        print(f"ERROR: {e}")
    driver.quit()


if __name__ == '__main__':
    main()
