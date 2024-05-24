import pyautogui
from pytest_bdd import when
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

import common
from page_objects.adt_login_page import ADTLoginPage
from step_definitions import login_steps

ADT_LOGIN_PAGE = ADTLoginPage()
PLATFORM_HOTKEYS = {
    'windows': [Keys.CONTROL, 'ctrl'],
    'mac': [Keys.COMMAND, 'command'],
    'linux': [Keys.CONTROL, 'control']
}
EXTENSION_NAME = "Five9 Agent Desktop Toolkit"


@when("I am in adt login page")
def see_adt_login_page():
    assert ADT_LOGIN_PAGE.url in ADT_LOGIN_PAGE.driver.current_url
