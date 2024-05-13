from selenium.webdriver.common.by import By


class CallInteractionPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.number_input = "//input[@id='MakeCallFilter-filter-input']"
        self.dial_button = "//button[@id='NewCallOptions-action-button']"
        self.dnc_dialog = "//div[@id='okay-cancel-dialog']"
        self.ok_dialog_button = "//button[@id='OkCancelDialog-ok-button']"
        self.cancel_dialog_button = "//button[@id='OkCancelDialog-cancel-button']"
        self.call_contact_header = "//span[@id='AgentVoiceDetailsHeader-contact-node']"
        self.call_notification_dialog = "//div[@id='call-notification-dialog']"
        self.call_notification_dialog_ok_button = "//button[@id='CallNotificationDialog-ok-button']"
        self.outbound_campaigns_button = "//button[@id='NewCallOptions-campaign-button']"
        self.outbound_campaigns_options = "//ul[contains(@class, 'campaign-dropdown')]/li"
        self.caller_contact = "//span[@class='info-contact']"
        self.interaction_tab = "//li[contains(@id, 'context')]/a"
        self.history_tab = "//li[contains(@id, 'history')]/a"
        self.script_tab = "//li[contains(@id, 'script')]/a"
        self.script_content = "//iframe[@id='custom-script']"
        self.script_title = "//span[contains(text(), 'Inbound Call Arriving')]"
        self.script_caller_data = "//td[@class='grey_box cell']"
        self.connector_tab = "//li[contains(@id, 'connector')]/a"
        self.worksheet_button = "//button[@id='AgentVoiceDetailsContentsButtons-worksheet-button']"
        self.worksheet_agent_screen_panel = "//div[@class='agent-screen-worksheet-panel']"
        self.worksheet_expand_button = "//button[@class='worksheet-expand']"
        self.worksheet_cancel_expand = "//a[@href='#'][text()='Cancel']"
        self.worksheet_move_to_panel = "//a[@href='#'][text()='Move to Panel']"
        self.worksheet_questions = "//div[@class='questionList']/div"
        self.worksheet_current_question = "//div[@class='worksheetQuestionNumber']"
        self.worksheet_next_question_button = "//button[contains(@class, 'ws_next_btn')]"
        self.worksheet_previous_question_button = "//button[contains(@class, 'ws_prev_btn')]"
        self.worksheet_finish_question_button = "//button[contains(@class, 'ws_finish_btnbtn')]"
        self.worksheet_question_answer_text_area = "//textarea[@id='ws_answer_line']"

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

    def get_call_contact_header(self):
        return self.driver.find_element(By.XPATH, self.call_contact_header)

    def get_call_notification_dialog(self):
        return self.driver.find_element(By.XPATH, self.call_notification_dialog)

    def get_call_notification_dialog_ok_button(self):
        return self.driver.find_element(By.XPATH, self.call_notification_dialog_ok_button)

    def get_outbound_campaigns_button(self):
        return self.driver.find_element(By.XPATH, self.outbound_campaigns_button)

    def get_outbound_campaigns_options(self):
        return self.driver.find_elements(By.XPATH, self.outbound_campaigns_options)

    def get_interaction_tab(self):
        return self.driver.find_element(By.XPATH, self.interaction_tab)

    def get_history_tab(self):
        return self.driver.find_element(By.XPATH, self.history_tab)

    def get_script_tab(self):
        return self.driver.find_element(By.XPATH, self.script_tab)

    def get_script_content(self):
        return self.driver.find_element(By.XPATH, self.script_content)

    def get_script_title(self):
        return self.driver.find_element(By.XPATH, self.script_title)

    def get_script_caller_data(self):
        return self.driver.find_elements(By.XPATH, self.script_caller_data)

    def get_connector_tab(self):
        return self.driver.find_element(By.XPATH, self.connector_tab)

    def get_worksheet_button(self):
        return self.driver.find_element(By.XPATH, self.worksheet_button)

    def get_worksheet_agent_screen_panel(self):
        return self.driver.find_element(By.XPATH, self.worksheet_agent_screen_panel)

    def get_worksheet_expand_button(self):
        return self.driver.find_element(By.XPATH, self.worksheet_expand_button)

    def get_worksheet_cancel_expand(self):
        return self.driver.find_element(By.XPATH, self.worksheet_cancel_expand)

    def get_worksheet_move_to_panel(self):
        return self.driver.find_element(By.XPATH, self.worksheet_move_to_panel)

    def get_worksheet_questions(self):
        return self.driver.find_elements(By.XPATH, self.worksheet_questions)

    def get_worksheet_current_question(self):
        return self.driver.find_element(By.XPATH, self.worksheet_current_question)

    def get_worksheet_next_question_button(self):
        return self.driver.find_element(By.XPATH, self.worksheet_next_question_button)

    def get_worksheet_previous_question_button(self):
        return self.driver.find_element(By.XPATH, self.worksheet_previous_question_button)

    def get_worksheet_finish_question_button(self):
        return self.driver.find_element(By.XPATH, self.worksheet_finish_question_button)

    def get_worksheet_question_answer_text_area(self):
        return self.driver.find_element(By.XPATH, self.worksheet_question_answer_text_area)
