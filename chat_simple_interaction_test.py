import common
from time import sleep
from page_objects.agent_home_page import AgentHomePage
from driver import Driver
from page_objects.chat_template_page import ChatTemplatePage
from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.station_setup_page import StationSetupPage


def main():
    url = "https://ondemand.eu-central-1.saucelabs.com:443/wd/hub"
    driver = Driver(url).driver
    driver2 = None

    try:
        # I perform login
        login_ = LoginPage(driver)
        login_.open_page()
        login_.get_user_input().send_keys('<five9_user>')
        login_.get_password_input().send_keys('<five9_pass>')
        login_.get_login_button().click()

        # I see the home page
        home_ = HomePage(driver)
        common.wait_page_element_load(driver, home_.agent_span)
        home_.get_agent_span().click()
        home_.get_web_agent_item().click()

        # I select adp from menu
        station_setup_ = StationSetupPage(driver)
        common.switch_tabs(driver)
        common.wait_page_element_load(driver, station_setup_.none_station, 120)
        station_setup_.get_none_station_type().click()
        station_setup_.get_next_button().click()

        # I change agent state to ready for text
        agent_home_ = AgentHomePage(driver)
        common.wait_page_element_load(driver, agent_home_.agent_activity_button, timeout_in_seconds=60)
        agent_home_.get_agent_status_button().click()
        agent_home_.get_ready_for_option().click()
        if "checked" not in agent_home_.get_text_channel_checkbox_status().get_attribute("class"):
            agent_home_.get_text_channel_checkbox().click()
            common.wait_element_class_contains(driver, agent_home_.text_channel_checkbox, "checked")
        agent_home_.get_confirm_channel_button().click()
        common.wait_element_class_contains(driver, agent_home_.agent_status_button, "state-ready")

        # I go to chat template page
        driver2 = Driver(url).driver
        chat_template_ = ChatTemplatePage(driver2)
        chat_template_.open_page()
        common.wait_element_to_be_clickable(driver2, chat_template_.open_chat_button)
        chat_template_.get_title_input().send_keys('Automatic chat')
        common.element_recursive_click(driver2, chat_template_.open_chat_button, 2)

        # I send a new message to the agent
        common.switch_to_frame(driver2, chat_template_.get_chat_frame())
        common.wait_page_element_load(driver2, chat_template_.name_input)
        chat_template_.get_name_input().send_keys('Automation Test User')
        chat_template_.get_email_input().send_keys('automation@test.user')
        common.wait_page_element_load(driver2, chat_template_.start_chat_button)
        sleep(2)
        chat_template_.get_question_textarea().send_keys("Automatic message")
        sleep(2)
        chat_template_.get_start_chat_button().click()
        common.wait_page_element_load(driver2, chat_template_.loading_message)

        # Agent check and accept the text interaction
        driver.switch_to.window(driver.current_window_handle)
        agent_home_.get_agent_chat_button().click()
        common.element_recursive_click(driver, agent_home_.refresh_chats_button, 20)  # 10s
        common.wait_element_to_be_more_than(driver, agent_home_.newest_chat_interaction, 1)
        agent_home_.get_unselected_lock_chat_button().click()
        agent_home_.get_newest_chat_interaction().click()  # select the newest even if more than 1 is displayed
        common.wait_page_element_load(driver, agent_home_.conversation_content)

        # Agent answer the message
        sleep(2)
        common.assert_condition("Automatic message" in agent_home_.get_conversation_content().text,
                                "CUSTOMER MESSAGE IS NOT BEING SENT TO AGENT")
        agent_home_.get_reply_message_textarea().send_keys("Automatic reply")
        agent_home_.get_send_message_button().click()

        # I check if agent message is displayed in customer chat
        driver2.switch_to.window(driver2.current_window_handle)
        common.switch_to_frame(driver2, chat_template_.get_chat_frame())
        sleep(2)
        common.assert_condition("Automatic reply" in chat_template_.get_chat_content().text,
                                "AGENT MESSAGE IS NOT BEING SENT TO CUSTOMER")

        # Agent dispose the chat interaction
        driver.switch_to.window(driver.current_window_handle)
        agent_home_.get_set_disposition_button().click()
        common.wait_page_element_load(driver, agent_home_.no_disposition_option)
        agent_home_.get_no_disposition_option().click()
        common.wait_elements_to_be_less_than(driver, agent_home_.newest_chat_interaction, 2)

        # I check if the chat interaction is closed
        driver2.switch_to.window(driver2.current_window_handle)
        common.switch_to_frame(driver2, chat_template_.get_chat_frame())
        common.wait_page_element_load(driver2, chat_template_.send_survey_button)
        common.assert_condition(chat_template_.get_send_survey_button().is_displayed(), "SEND SURVEY BUTTON IS NOT BEING DISPLAYED")

        # logout user
        driver.switch_to.window(driver.current_window_handle)
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
    if driver2:
        driver2.quit()


if __name__ == '__main__':
    main()
