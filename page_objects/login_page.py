# all the elements of Login Page should be here
import common
from selenium.webdriver.common.by import By


class LoginPage(object):
    def __init__(self, driver):
        self.driver = driver
        self.user_input = "//input[@id='username']"
        self.pass_input = "//input[@id='password']"
        self.login_button = "//input[@id='loginBtn']"
        self.credentials = common.get_config_file_section('../config.ini', 'credentials')
        self.url = 'https://login.eu.five9.com/'

    def open_page(self):
        self.driver.get(self.url)

    def get_url(self):
        return self.url

    def get_user_input(self):
        return self.driver.find_element(By.XPATH, self.user_input)

    def get_password_input(self):
        return self.driver.find_element(By.XPATH, self.pass_input)

    def get_login_button(self):
        return self.driver.find_element(By.XPATH, self.login_button)
