from selenium.webdriver.common.by import By


class CommonPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.connector_url = None
        self.modal_dialog = "//div[@class='f9-modal-dialog'][contains(., '<title>')]"
        self.modal_submit_button = "//button[contains(@class, 'f9-positive-cta-btn') and contains(., '<text>')]"
        self.modal_back_button = "//button[@id='WizardBase-back-button']"
        self.available_skills = "//div[@data-f9-template='agent-skill-select-item']/label | //ul[@id='skills_list']//label"
        self.all_skills_button = "//button[@id='agent-skill-select-toggle'] | //input[@id='all_skills']"
        self.modal_dialog_skills_sf = "//div[@data-f9-template='agent-skill-select']//h1[contains(., '<title>')]"

    def get_modal_dialog(self, title=None):
        return self.driver.find_element(By.XPATH, self.modal_dialog.replace("<title>", title))

    def get_modal_submit_button(self, text_):
        return self.driver.find_element(By.XPATH, self.modal_submit_button.replace('<text>', text_))

    def get_modal_back_button(self):
        return self.driver.find_element(By.XPATH, self.modal_back_button)

    def get_available_skills(self):
        return self.driver.find_elements(By.XPATH, self.available_skills)

    def get_all_skills_button(self):
        return self.driver.find_element(By.XPATH, self.all_skills_button)
