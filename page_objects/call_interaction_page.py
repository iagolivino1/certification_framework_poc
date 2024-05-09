from selenium.webdriver.common.by import By


class CallInteractionPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.number_input = "//input[@id='MakeCallFilter-filter-input']"
        self.dial_button = "//button[@id='NewCallOptions-action-button']"
        self.dnc_dialog = "//div[@id='okay-cancel-dialog']"
        self.ok_dialog_button = "//button[@id='OkCancelDialog-ok-button']"
        self.cancel_dialog_button = "//button[@id='OkCancelDialog-cancel-button']"
        self.call_notification_dialog = "//div[@id='call-notification-dialog']"
        self.call_notification_dialog_ok_button = "//button[@id='CallNotificationDialog-ok-button']"
        self.outbound_campaigns_button = "//button[@id='NewCallOptions-campaign-button']"
        self.outbound_campaigns_options = "//ul[contains(@class, 'campaign-dropdown')]/li"

    def get_number_input(self):
        return self.driver.find_element(By.XPATH, self.number_input)

    def get_dial_button(self):
        return self.driver.find_element(By.XPATH, self.dial_button)

    def get_dnc_dialog(self):
        return self.driver.find_element(By.XPATH, self.dnc_dialog)

    def get_ok_dialog_button(self):
        return self.driver.find_element(By.XPATH, self.ok_dialog_button)

    def get_cancel_dialog_button(self):
        return self.driver.find_element(By.XPATH, self.cancel_dialog_button)

    def get_call_notification_dialog(self):
        return self.driver.find_element(By.XPATH, self.call_notification_dialog)

    def get_call_notification_dialog_ok_button(self):
        return self.driver.find_element(By.XPATH, self.call_notification_dialog_ok_button)

    def get_outbound_campaigns_button(self):
        return self.driver.find_element(By.XPATH, self.outbound_campaigns_button)

    def get_outbound_campaigns_options(self):
        return self.driver.find_elements(By.XPATH, self.outbound_campaigns_options)
