from selenium.webdriver.common.by import By


class ChatInteractionPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.newest_chat_interaction = "//div[@class='ReactVirtualized__Grid__innerScrollContainer']//li"
        self.unselected_lock_chat_button = self.newest_chat_interaction+"//i[contains(@class, 'fa-unlock')]"
        self.selected_lock_chat_button = self.newest_chat_interaction+"//i[contains(@class, 'fa-lock')]"
        self.refresh_chats_button = "//div[@id='refresh-button']"
        self.accept_chat_button = "//button[@class='btn f9-standard-btn accept tt tt-allow-content']"
        self.reject_chat_button = "//button[@class='btn f9-standard-btn reject tt tt-allow-content']"
        self.conversation_content = "//div[@class='container-conversation']"
        self.reply_message_textarea = "//div[contains(@class, 'container-reply-message')]//textarea"
        self.send_message_button = "//button[@id='ChatDetailsActions-send-button']"
        self.set_disposition_button = "//button[@id='ReactSearchableDropdown-searchabledropdown-button']"

    def get_set_disposition_button(self):
        return self.driver.find_element(By.XPATH, self.set_disposition_button)

    def get_newest_chat_interaction(self):
        return self.driver.find_element(By.XPATH, self.newest_chat_interaction)

    def get_all_chat_interactions(self):
        return self.driver.find_elements(By.XPATH, self.newest_chat_interaction)

    def get_selected_lock_chat_button(self):
        return self.driver.find_element(By.XPATH, self.selected_lock_chat_button)

    def get_all_selected_lock_chat_buttons(self):
        return self.driver.find_elements(By.XPATH, self.selected_lock_chat_button)

    def get_unselected_lock_chat_button(self):
        return self.driver.find_element(By.XPATH, self.unselected_lock_chat_button)

    def get_all_unselected_lock_chat_buttons(self):
        return self.driver.find_elements(By.XPATH, self.unselected_lock_chat_button)

    def get_refresh_chats_button(self):
        return self.driver.find_element(By.XPATH, self.refresh_chats_button)

    def get_accept_chat_button(self):
        return self.driver.find_element(By.XPATH, self.accept_chat_button)

    def get_reject_chat_button(self):
        return self.driver.find_element(By.XPATH, self.reject_chat_button)

    def get_conversation_content(self):
        return self.driver.find_element(By.XPATH, self.conversation_content)

    def get_reply_message_textarea(self):
        return self.driver.find_element(By.XPATH, self.reply_message_textarea)

    def get_send_message_button(self):
        return self.driver.find_element(By.XPATH, self.send_message_button)