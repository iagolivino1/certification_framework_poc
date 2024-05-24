from selenium.webdriver.common.by import By


class ADTAdapterPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.url = ''
        self.content_header = "//h1"
        self.station_setup = "//div[@data-f9-template='station-setup-container']"
        self.softphone_station_option = "//ul[@id='station_types_list']//input[@id='station_SOFTPHONE']"
        self.webrtc_station_option = "//ul[@id='station_types_list']//input[@id='station_WEBRTC']"
        self.pstn_station_option = "//ul[@id='station_types_list']//input[@id='station_PSTN']"
        self.gateway_station_option = "//ul[@id='station_types_list']//input[@id='station_GATEWAY']"
        self.none_station_option = "//ul[@id='station_types_list']//input[@id='station_EMPTY']"
        self.station_number_input = "//input[@id='station_number']"
        self.confirm_selection_button = "//button[text()='Confirm']"
        self.station_setup_devices = "//div[@data-f9-template='setup-devices']"
        self.reset_station_button = "//button[@id='restart-softphone']"
        self.station_connection_status = "//div[@class='softphone-status-bar']//span[not(contains(@class, 'stationType'))]"
        self.loading_label = "//i[@class='fa fa-spinner fa-spin']/.."

    def get_content_header(self):
        return self.driver.find_element(By.XPATH, self.content_header)

    def get_station_setup(self):
        return self.driver.find_element(By.XPATH, self.station_setup)

    def get_softphone_station_option(self):
        return self.driver.find_element(By.XPATH, self.softphone_station_option)

    def get_webrtc_station_option(self):
        return self.driver.find_element(By.XPATH, self.webrtc_station_option)

    def get_pstn_station_option(self):
        return self.driver.find_element(By.XPATH, self.pstn_station_option)

    def get_gateway_station_option(self):
        return self.driver.find_element(By.XPATH, self.gateway_station_option)

    def get_none_station_option(self):
        return self.driver.find_element(By.XPATH, self.none_station_option)

    def get_station_number_input(self):
        return self.driver.find_element(By.XPATH, self.station_number_input)

    def get_confirm_selection_button(self):
        return self.driver.find_element(By.XPATH, self.confirm_selection_button)

    def get_station_setup_devices(self):
        return self.driver.find_element(By.XPATH, self.station_setup_devices)

    def get_reset_station_button(self):
        return self.driver.find_element(By.XPATH, self.reset_station_button)

    def get_station_connection_status(self):
        return self.driver.find_element(By.XPATH, self.station_connection_status)

    def get_loading_label(self):
        return self.driver.find_element(By.XPATH, self.loading_label)
