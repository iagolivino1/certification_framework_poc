from selenium.webdriver.common.by import By


class AgentHomePage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.agent_status_button = "//button[@id='ReadyCodesLayout-ready-button']"
        self.ready_for_current_option = "//a[@id='ReadyCodesLayout-readycurrent-label']"
        self.ready_for_option = "//a[@id='ReadyCodesLayout-readyfor-label']"
        self.agent_home_button = "//a[@id='AgentLeftNavbarItem-home-button']"
        self.agent_voice_button = "//a[@id='AgentLeftNavbarItem-voice-button']"
        self.agent_voicemail_button = "//a[@id='AgentLeftNavbarItem-voicemail-button']"
        self.agent_chat_button = "//a[@id='AgentLeftNavbarItem-chat-button']"
        self.agent_email_button = "//a[@id='AgentLeftNavbarItem-email-button']"
        self.agent_crm_button = "//a[@id='AgentLeftNavbarItem-crm-button']"
        self.agent_activity_button = "//a[@id='AgentLeftNavbarItem-activity-button']"
        self.agent_profile_button = "(//button[@class='btn btn-link tt dropdown-toggle'])[last()]"
        self.agent_logout_element = "//a[@data-id='logout']"
        self.logout_reason_dialog = "//div[@id='logout-reason-dialog']"
        self.confirm_logout_button = "//button[@id='LogoutReasonDialog-confirm-button']"
        self.voice_channel_checkbox = "//ul[@class='channels-list']//button[@id='call']"
        self.voice_channel_checkbox_status = "//ul[@class='channels-list']//button[@id='call']/div"
        self.voicemail_channel_checkbox = "//ul[@class='channels-list']//button[@id='voice_mail']"
        self.voicemail_channel_checkbox_status = "//ul[@class='channels-list']//button[@id='voice_mail']/div"
        self.text_channel_checkbox = "//ul[@class='channels-list']//button[@id='text']"
        self.text_channel_checkbox_status = "//ul[@class='channels-list']//button[@id='text']/div"
        self.confirm_channel_button = "//button[@id='ReadyForDialog-ok-button']"
        self.cancel_channel_button = "//button[@id='ReadyForDialog-cancel-button']"
        self.set_disposition_button = "//span[contains(text(), 'SET DISPOSITION')]/.."
        self.no_disposition_option = "//a[text()='No Disposition']"
        self.do_not_call_disposition_option = "//a[text()='Do Not Call']"
        self.do_not_call_disposition_option = "//a[text()='Do Not Call']"
        self.all_dispositions = "//ul[contains(@class, 'voice-dispositions')]/li/a"

    def get_agent_status_button(self):
        return self.driver.find_element(By.XPATH, self.agent_status_button)

    def get_ready_for_current_option(self):
        return self.driver.find_element(By.XPATH, self.ready_for_current_option)

    def get_ready_for_option(self):
        return self.driver.find_element(By.XPATH, self.ready_for_option)

    def get_agent_home_button(self):
        return self.driver.find_element(By.XPATH, self.agent_home_button)

    def get_agent_voice_button(self):
        return self.driver.find_element(By.XPATH, self.agent_voice_button)

    def get_agent_voicemail_button(self):
        return self.driver.find_element(By.XPATH, self.agent_voicemail_button)

    def get_agent_chat_button(self):
        return self.driver.find_element(By.XPATH, self.agent_chat_button)

    def get_agent_email_button(self):
        return self.driver.find_element(By.XPATH, self.agent_email_button)

    def get_agent_crm_button(self):
        return self.driver.find_element(By.XPATH, self.agent_crm_button)

    def get_agent_activity_button(self):
        return self.driver.find_element(By.XPATH, self.agent_activity_button)

    def get_agent_profile_button(self):
        return self.driver.find_element(By.XPATH, self.agent_profile_button)

    def get_agent_logout_element(self):
        return self.driver.find_element(By.XPATH, self.agent_logout_element)

    def get_logout_reason_dialog(self):
        return self.driver.find_element(By.XPATH, self.logout_reason_dialog)

    def get_confirm_logout_button(self):
        return self.driver.find_element(By.XPATH, self.confirm_logout_button)

    def get_voice_channel_checkbox(self):
        return self.driver.find_element(By.XPATH, self.voice_channel_checkbox)

    def get_voice_channel_checkbox_status(self):
        return self.driver.find_element(By.XPATH, self.voice_channel_checkbox_status)

    def get_voicemail_channel_checkbox(self):
        return self.driver.find_element(By.XPATH, self.voicemail_channel_checkbox)

    def get_voicemail_channel_checkbox_status(self):
        return self.driver.find_element(By.XPATH, self.voicemail_channel_checkbox_status)

    def get_text_channel_checkbox(self):
        return self.driver.find_element(By.XPATH, self.text_channel_checkbox)

    def get_text_channel_checkbox_status(self):
        return self.driver.find_element(By.XPATH, self.text_channel_checkbox_status)

    def get_confirm_channel_button(self):
        return self.driver.find_element(By.XPATH, self.confirm_channel_button)

    def get_cancel_channel_button(self):
        return self.driver.find_element(By.XPATH, self.cancel_channel_button)

    def get_set_disposition_button(self):
        return self.driver.find_element(By.XPATH, self.set_disposition_button)

    def get_no_disposition_option(self):
        return self.driver.find_element(By.XPATH, self.no_disposition_option)

    def get_do_not_call_disposition_option(self):
        return self.driver.find_element(By.XPATH, self.do_not_call_disposition_option)

    def get_all_dispositions(self):
        return self.driver.find_elements(By.XPATH, self.all_dispositions)
