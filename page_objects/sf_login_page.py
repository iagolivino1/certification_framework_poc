from selenium.webdriver.common.by import By

class SFLoginPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.user_input = "//input[@id='username'] | //input[@id='email']"
        self.pass_input = "//input[@id='password']"
        self.login_button = "//input[@id='Login'] | //button[@id='submitButton']"
        self.logo_img = "//img[@id='phHeaderLogoImage'] | //div[@id='uif35']"
        self.sf_url = "https://login.salesforce.com/"
        self.ns_url = "https://system.netsuite.com/pages/customerlogin.jsp?country=US"
        self.ns_additional_auth_title = "//div[@class='roleswitch-title']/h1"
        self.ns_additional_pass = "//input[@name='answer']"
        self.ns_additional_submit_btn = "//input[@name='submitter']"

    def open_page(self, url="https://login.salesforce.com/"):
        self.driver.get(url)

    def get_salesforce_url(self):
        return self.sf_url
    
    def get_netsuite_url(self):
        return self.ns_url

    def get_user_input(self):
        return self.driver.find_element(By.XPATH, self.user_input)

    def get_password_input(self):
        return self.driver.find_element(By.XPATH, self.pass_input)

    def get_login_button(self):
        return self.driver.find_element(By.XPATH, self.login_button)
    
    def get_logo_img(self):
        return self.driver.find_element(By.XPATH, self.logo_img)
    
    def get_ns_additional_auth_title(self):
        return self.driver.find_element(By.XPATH, self.ns_additional_auth_title)
    
    def get_ns_additional_pass(self):
        return self.driver.find_element(By.XPATH, self.ns_additional_pass)
    
    def get_ns_additional_submit_btn(self):
        return self.driver.find_element(By.XPATH, self.ns_additional_submit_btn)