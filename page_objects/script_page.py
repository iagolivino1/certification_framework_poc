from selenium.webdriver.common.by import By


class ScriptPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.script_content = "//iframe[@id='custom-script']"
        self.header = "//table[1]//td[2]/span"
        self.description = "//td/div"
        self.subscriber_data_table = "//table[3]"
        self.customer_name = "//table[3]//tr[1]/td[2]"
        self.street = "//table[3]//tr[2]/td[2]"
        self.address = "//table[3]//tr[3]/td[2]"
        self.phone_number = "//table[3]//tr[4]/td[2]"

    def get_script_content(self):
        return self.driver.find_element(By.XPATH, self.script_content)

    def get_header(self):
        return self.driver.find_element(By.XPATH, self.header)

    def get_description(self):
        return self.driver.find_element(By.XPATH, self.description)

    def get_subscriber_data_table(self):
        return self.driver.find_element(By.XPATH, self.subscriber_data_table)

    def get_customer_name(self):
        return self.driver.find_element(By.XPATH, self.customer_name)

    def get_street(self):
        return self.driver.find_element(By.XPATH, self.street)

    def get_address(self):
        return self.driver.find_elements(By.XPATH, self.address)

    def get_phone_number(self):
        return self.driver.find_element(By.XPATH, self.phone_number)