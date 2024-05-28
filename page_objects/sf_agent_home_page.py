from selenium.webdriver.common.by import By


class SFAgentHomePage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.logo_img = "//img[@id='phHeaderLogoImage']"
        self.agent_state_button = "//button[@id='agent-readyState']"
        self.new_call_btn = "//button[@id='newCall-btn']"
        self.softphone_iframe = "//iframe[@id='SoftphoneIframe']"
        self.iframe_user_input = "//input[@id='username']"
        self.agent_call_panel = "//div[@id='callPanel']"

    def get_agent_state_button(self):
        return self.driver.find_element(By.XPATH, self.agent_state_button)
    
    def get_new_call_btn(self):
        return self.driver.find_element(By.XPATH, self.new_call_btn)
    
    def get_iframe_softphone(self):
        return self.driver.find_element(By.XPATH, self.softphone_iframe)
    
    def get_iframe_login_btn(self):
        return self.driver.find_element(By.XPATH, self.iframe_user_input)
    
    def get_logo_img(self):
        return self.driver.find_element(By.XPATH, self.logo_img)