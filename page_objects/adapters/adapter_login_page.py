from selenium.webdriver.common.by import By


class AdapterLoginPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.url = "https://qaapp01d.five9lab.com/clients/integrations/adt.main.html"
        self.adapter_user_input = "//input[@id='username']"
        self.adapter_pass_input = "//input[@id='password']"
        self.adapter_login_button = "//button[contains(@id,'login_btn')]"
        self.force_login_button = "//button[@id='force-login']"

    def open_page(self):
        self.driver.get(self.url)

    def get_adapter_user_input(self):
        return self.driver.find_element(By.XPATH, self.adapter_user_input)

    def get_adapter_password_input(self):
        return self.driver.find_element(By.XPATH, self.adapter_pass_input)

    def get_adapter_login_button(self):
        return self.driver.find_element(By.XPATH, self.adapter_login_button)
    
    def get_force_login_button(self):
        return self.driver.find_element(By.XPATH, self.force_login_button)
