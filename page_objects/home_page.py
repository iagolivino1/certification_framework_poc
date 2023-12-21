# all the elements of Home Page should be here
from selenium.webdriver.common.by import By


class HomePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.logout_element = "//a[@id='page_logout']"
        self.agent_span = "//span[@id='app_agent_span']"
        self.web_agent_item = "//a[@id='web_agent_item']"
        self.logout_element = "//a[@id='page_logout']"
        self.url = "https://env.frk1.eu.five9.com/"

    def open_page(self):
        self.driver.get(self.url)

    def get_url(self):
        return self.url

    def get_logout_element(self):
        return self.driver.find_element(By.XPATH, self.logout_element)

    def get_agent_span(self):
        return self.driver.find_element(By.XPATH, self.agent_span)

    def get_web_agent_item(self):
        return self.driver.find_element(By.XPATH, self.web_agent_item)

    def get_logout_element(self):
        return self.driver.find_element(By.XPATH, self.logout_element)

