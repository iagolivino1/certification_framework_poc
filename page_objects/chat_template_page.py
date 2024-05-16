from selenium.webdriver.common.by import By


class ChatTemplatePage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.url = ""
        self.open_chat_button = "//div[@id='five9-maximize-button']"
        self.title_input = "//input[@id='five9-title']"
        self.start_chat_button = "//button[@id='start-chat-button']"
        self.chat_frame = "//iframe[@id='embedded-frame']"
        self.profile_dropdown = "//div[@id='profiles-button']/select"
        self.name_input = "//input[@id='name']"
        self.email_input = "//input[@id='email']"
        self.question_textarea = "//textarea[@id='question']"
        self.loading_message = "//div[@id='connecting-message']"
        self.input_message = "//textarea[@id='input-message']"
        self.send_message_button = "//button[@id='send-button']"
        self.chat_content = "//div[@class='chat-content ui-content']"
        self.end_conversation_button = "//a[@id='terminate-conversation-button']"
        self.end_who = "//div[@class='end-who']"
        self.send_survey_button = "//button[@id='send-survey-button']"
        self.end_chat_popup = "//div[@id='conversation-terminate-chat-popup']"
        self.end_chat_popup_button = "//div[@id='conversation-terminate-chat-popup']//a[text()='End Chat']"
        self.cancel_chat_popup_button = "//div[@id='conversation-terminate-chat-popup']//a[text()='Cancel']"

    def open_page(self):
        self.driver.get(self.url)

    def get_open_chat_button(self):
        return self.driver.find_element(By.XPATH, self.open_chat_button)

    def get_title_input(self):
        return self.driver.find_element(By.XPATH, self.title_input)

    def get_start_chat_button(self):
        return self.driver.find_element(By.XPATH, self.start_chat_button)

    def get_chat_frame(self):
        return self.driver.find_element(By.XPATH, self.chat_frame)

    def get_profile_dropdown(self):
        return self.driver.find_element(By.XPATH, self.profile_dropdown)

    def get_name_input(self):
        return self.driver.find_element(By.XPATH, self.name_input)

    def get_email_input(self):
        return self.driver.find_element(By.XPATH, self.email_input)

    def get_question_textarea(self):
        return self.driver.find_element(By.XPATH, self.question_textarea)

    def get_loading_message(self):
        return self.driver.find_element(By.XPATH, self.loading_message)

    def get_send_message_button(self):
        return self.driver.find_element(By.XPATH, self.send_message_button)

    def get_chat_content(self):
        return self.driver.find_element(By.XPATH, self.chat_content)

    def get_end_conversation_button(self):
        return self.driver.find_element(By.XPATH, self.end_conversation_button)

    def get_end_who(self):
        return self.driver.find_element(By.XPATH, self.end_who)

    def get_send_survey_button(self):
        return self.driver.find_element(By.XPATH, self.send_survey_button)

    def get_end_chat_popup(self):
        return self.driver.find_element(By.XPATH, self.end_chat_popup)

    def get_end_chat_popup_button(self):
        return self.driver.find_element(By.XPATH, self.end_chat_popup_button)

    def get_cancel_chat_popup_button(self):
        return self.driver.find_element(By.XPATH, self.cancel_chat_popup_button)
