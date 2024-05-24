from selenium.webdriver.common.by import By


class LoginPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.user_input = "//input[@id='username'] | //input[@id='Login-username-input']"
        self.pass_input = "//input[@id='password'] | //input[@id='Login-password-input']"
        self.login_button = "//input[@id='loginBtn'] | //button[@id='Login-login-button']"
        self.force_login_button = "//button[@id='force-login']"
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
    
    def get_force_login_button(self):
        return self.driver.find_element(By.XPATH, self.force_login_button)
