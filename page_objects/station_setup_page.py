# all the elements of Station Setup Page (it is a modal) should be here
from selenium.webdriver.common.by import By


class StationSetupPage(object):
    def __init__(self, driver):
        self.driver = driver
        self.setup_modal = "//div[@id='agent-prep-wizard']//div[contains(@class, 'f9-modal-dialog')]"
        self.none_station = "//label[@id='EMPTY']"
        self.softphone_station = "//label[@id='SOFTPHONE']"
        self.softphone_station_input = "//input[@id='SoftPhoneSetup-stationid-input']"
        self.next_button = "//button[@id='WizardBase-submit-button']"
        self.logout_button = "//button[@id='WizardBase-back-button']"

    def get_none_station_type(self):
        return self.driver.find_element(By.XPATH, self.none_station)

    def get_softphone_station_type(self):
        return self.driver.find_element(By.XPATH, self.softphone_station)

    def get_softphone_station_input(self):
        return self.driver.find_element(By.XPATH, self.softphone_station_input)

    def get_next_button(self):
        return self.driver.find_element(By.XPATH, self.next_button)

    def get_logout_button(self):
        return self.driver.find_element(By.XPATH, self.logout_button)
