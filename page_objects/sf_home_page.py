from selenium.webdriver.common.by import By


class SFHomePage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.logo_img = "//img[@id='phHeaderLogoImage']"
        self.logout_element = "//a[@id='page_logout']"
        self.agent_span = "//span[@id='app_agent_span']"
        self.web_agent_item = "//a[@id='web_agent_item']"
        self.softphone_iframe = "//iframe[@id='SoftphoneIframe']"
        self.iframe_user_input = "//input[@id='username']"
        self.url = "https://five9qademo1.my.salesforce.com/home/home.jsp"

    def open_page(self):
        self.driver.get(self.url)

    def get_url(self):
        return self.url

    def get_logout_element(self):
        return self.driver.find_element(By.XPATH, self.logout_element)

    def get_logo_img(self):
        return self.driver.find_element(By.XPATH, self.agent_span)

    def get_web_agent_item(self):
        return self.driver.find_element(By.XPATH, self.web_agent_item)

    def get_logout_element(self):
        return self.driver.find_element(By.XPATH, self.logout_element)
    
    def get_iframe_softphone(self):
        return self.driver.find_element(By.XPATH, self.softphone_iframe)
    
    def get_iframe_login_btn(self):
        return self.driver.find_element(By.XPATH, self.iframe_user_input)

