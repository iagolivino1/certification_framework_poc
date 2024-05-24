from selenium.webdriver.common.by import By


class SFAgentHomePage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.agent_state_button = "//button[@id='agent-readyState']"

    def get_agent_state_button(self):
        return self.driver.find_element(By.XPATH, self.agent_state_button)