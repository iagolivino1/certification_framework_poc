from selenium.webdriver.common.by import By


class ADTWorksheetPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.worksheet_questions = "//div[@id='ws_ql_wrapper']//li"
        self.worksheet_current_question = "//div[@id='ws_ql_wrapper']//li[@class='active']"
        self.worksheet_answers_textarea = "//textarea[@id='ws_answer_line']"
        self.worksheet_cancel_button = "//button[@id='ws_cancel_btn']"
        self.worksheet_finish_button = "//button[@id='ws_finish_btn']"
        self.worksheet_previous_button = "//button[@id='ws_prev_btn']"
        self.worksheet_next_button = "//button[@id='ws_next_btn']"

    def get_worksheet_questions(self):
        return self.driver.find_elements(By.XPATH, self.worksheet_questions)

    def get_worksheet_current_question(self):
        return self.driver.find_element(By.XPATH, self.worksheet_current_question)

    def get_worksheet_answers_textarea(self):
        return self.driver.find_element(By.XPATH, self.worksheet_answers_textarea)

    def get_worksheet_cancel_button(self):
        return self.driver.find_element(By.XPATH, self.worksheet_cancel_button)

    def get_worksheet_finish_button(self):
        return self.driver.find_element(By.XPATH, self.worksheet_finish_button)

    def get_worksheet_previous_button(self):
        return self.driver.find_element(By.XPATH, self.worksheet_previous_button)

    def get_worksheet_next_button(self):
        return self.driver.find_element(By.XPATH, self.worksheet_next_button)
