from selenium.webdriver.common.by import By

class SFLoginPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.user_input = "//input[@id='username']"
        self.pass_input = "//input[@id='password']"
        self.login_button = "//input[@id='Login']"
        self.logo_img = "//img[@id='phHeaderLogoImage']"
        self.url = 'https://login.salesforce.com/'

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
    
    def get_logo_img(self):
        return self.driver.find_element(By.XPATH, self.logo_img)