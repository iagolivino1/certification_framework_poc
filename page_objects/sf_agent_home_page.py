from selenium.webdriver.common.by import By


class SFAgentHomePage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.logo_img = "//img[@id='phHeaderLogoImage']"
        self.agent_state_button = "//button[@id='agent-readyState']"
        self.agent_ready_for_option = "//li[@id='ready_state_ready_for']"
        self.new_call_btn = "//button[@id='newCall-btn']"
        self.softphone_iframe = "//iframe[@id='SoftphoneIframe']"
        self.iframe_user_input = "//input[@id='username']"
        self.agent_call_panel = "//div[@id='callPanel']"
        self.set_disposition_btn = "//button[@id='call_endInteractionBtn']"
        self.select_disposition_radio_btn = "//div[@id='dispFilteredList_call']//label[contains(@title, '<text>')]"
        self.end_interaction_btn = "//button[@id='setDisposition_call']"
        self.channels_lst = "//ul[@id='channels_list']/li"
        self.text_channel_checkbox = "//label[@for='channel_TEXT']"
        self.text_channel_input = "//input[@id='channel_TEXT']"
        self.voice_channel_checkbox = "//label[@for='channel_CALL']"
        self.voice_channel_input = "//input[@id='channel_CALL']"
        self.voicemail_channel_checkbox = "//label[@for='channel_VOICE_MAIL']"
        self.voicemail_channel_input = "//input[@id='channel_VOICE_MAIL']"
        self.channels_confirm_btn = "//button[@id='channels_confirm_btn']"

    def get_agent_state_button(self):
        return self.driver.find_element(By.XPATH, self.agent_state_button)
    
    def get_agent_ready_for_option(self):
        return self.driver.find_element(By.XPATH, self.agent_ready_for_option)
    
    def get_text_channel_checkbox(self):
        return self.driver.find_element(By.XPATH, self.text_channel_checkbox)
    
    def get_text_channel_input(self):
        return self.driver.find_element(By.XPATH, self.text_channel_input)
    
    def get_voice_channel_checkbox(self):
        return self.driver.find_element(By.XPATH, self.voice_channel_checkbox)
    
    def get_voice_channel_input(self):
        return self.driver.find_element(By.XPATH, self.voice_channel_input)
    
    def get_voicemail_channel_checkbox(self):
        return self.driver.find_element(By.XPATH, self.voicemail_channel_checkbox)
    
    def get_voicemail_channel_input(self):
        return self.driver.find_element(By.XPATH, self.voicemail_channel_input)
    
    def get_new_call_btn(self):
        return self.driver.find_element(By.XPATH, self.new_call_btn)
    
    def get_iframe_softphone(self):
        return self.driver.find_element(By.XPATH, self.softphone_iframe)
    
    def get_iframe_login_btn(self):
        return self.driver.find_element(By.XPATH, self.iframe_user_input)
    
    def get_logo_img(self):
        return self.driver.find_element(By.XPATH, self.logo_img)
    
    def get_set_disposition_button(self):
        return self.driver.find_element(By.XPATH, self.set_disposition_btn)
    
    def get_select_disposition_radio_btn(self, text):
        return self.driver.find_element(By.XPATH, self.select_disposition_radio_btn.replace('<text>', text))
    
    def get_end_interaction_btn(self):
        return self.driver.find_element(By.XPATH, self.end_interaction_btn)
    
    def get_channels_list(self):
        return self.driver.find_elements(By.XPATH, self.channels_lst)
    
    def get_channel_property(self, elm, extender):
        return elm.find_element(By.XPATH, extender)
    
    def get_channels_confirm_btn(self):
        return self.driver.find_element(By.XPATH, self.channels_confirm_btn)