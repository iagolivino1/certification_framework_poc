# all the elements of Station Setup Page (it is a modal) should be here
from selenium.webdriver.common.by import By


class StationSetupPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.setup_modal = "//div[@id='agent-prep-wizard']//div[contains(@class, 'f9-modal-dialog')]"
        self.none_station = "//label[@id='EMPTY']"
        self.softphone_station = "//label[@id='SOFTPHONE']"
        self.webrtc_station = "//label[@id='WEBRTC']"
        self.pstn_station = "//label[@id='PSTN']"
        self.gateway_station = "//label[@id='GATEWAY']"
        self.station_input = "//input[contains(@id, '-stationid-input')]"
        self.station_tone_check_status = "//div[@id='station-tone-check-status']/span"
        self.restart_station_button = "//button[@id='restartStationBtn']"

    def get_none_station_type(self):
        return self.driver.find_element(By.XPATH, self.none_station)

    def get_softphone_station_type(self):
        return self.driver.find_element(By.XPATH, self.softphone_station)

    def get_webrtc_station_type(self):
        return self.driver.find_element(By.XPATH, self.webrtc_station)

    def get_pstn_station_type(self):
        return self.driver.find_element(By.XPATH, self.pstn_station)

    def get_gateway_station_type(self):
        return self.driver.find_element(By.XPATH, self.gateway_station)

    def get_station_input(self):
        return self.driver.find_elements(By.XPATH, self.station_input)

    def get_station_tone_check_status(self):
        return self.driver.find_element(By.XPATH, self.station_tone_check_status)

    def get_restart_station_button(self):
        return self.driver.find_element(By.XPATH, self.restart_station_button)
