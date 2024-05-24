import pyautogui, os
from pytest_bdd import when
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

import common
from page_objects.adt_login_page import ADTLoginPage
from step_definitions import login_steps

ADT_LOGIN_PAGE = ADTLoginPage()


def set_adapter_url(extension_id):
    ADT_LOGIN_PAGE.driver.get(f"chrome-extension://{extension_id}/options.html")
    common.system_wait(2)

    # set extension url
    input_url = ADT_LOGIN_PAGE.driver.find_element(By.XPATH, "//input[@id='url']")
    input_url.clear()
    input_url.click()
    input_url.send_keys(ADT_LOGIN_PAGE.url)
    try:
        assert input_url.get_attribute('value') == ADT_LOGIN_PAGE.url
    except AssertionError:
        input_url.clear()
        input_url.send_keys(ADT_LOGIN_PAGE.url)
        assert input_url.get_attribute('value') == ADT_LOGIN_PAGE.url, "COULD NOT SET THE CORRECT URL"
    ADT_LOGIN_PAGE.driver.find_element(By.XPATH, "//button[@id='save']").click()
    common.wait_element_attribute_contains(ADT_LOGIN_PAGE.driver, "//mark[@id='status']", 'innerText', "Options Saved")


@when("I am in adt login page")
def see_adt_login_page():
    # find the extension
    extension_text = "Five9 Agent Desktop Toolkit"
    ADT_LOGIN_PAGE.driver.get("chrome://extensions")
    extension_manager_element_shadow = ADT_LOGIN_PAGE.driver.find_element(By.XPATH, "//extensions-manager")
    extension_items_list_shadow = extension_manager_element_shadow.shadow_root.find_element(By.CSS_SELECTOR, "#items-list")
    extensions = extension_items_list_shadow.shadow_root.find_elements(By.CSS_SELECTOR, "extensions-item")
    selected_extension = None
    for extension in extensions:
        extension_name = extension.shadow_root.find_element(By.CSS_SELECTOR, "#name").text.strip()
        if extension_name == extension_text:
            selected_extension = extension
            break
    if not selected_extension:
        raise Exception(f"extension {extension_text} not found")

    # open extension options
    selected_extension.shadow_root.find_element(By.CSS_SELECTOR, "#detailsButton").click()
    common.wait_page_to_be(ADT_LOGIN_PAGE.driver, "?id=")
    extension_id = ADT_LOGIN_PAGE.driver.current_url.split("?id=")[1].strip()

    left_panel_shadow = extension_manager_element_shadow.shadow_root.find_element(By.CSS_SELECTOR, "extensions-sidebar")
    keyboard_shortcuts = left_panel_shadow.shadow_root.find_element(By.CSS_SELECTOR, "a#sectionsShortcuts")
    keyboard_shortcuts.click()

    keyboard_shortcuts_content_shadow = extension_manager_element_shadow.shadow_root.find_element(By.CSS_SELECTOR, "extensions-keyboard-shortcuts")
    extension_cards = keyboard_shortcuts_content_shadow.shadow_root.find_elements(By.CSS_SELECTOR, ".shortcut-card")
    selected_extension_card = None
    for extension_card in extension_cards:
        if extension_text in extension_card.text:
            selected_extension_card = extension_card
            break
    if not selected_extension_card:
        raise Exception(f"card for {extension_text} extension not found")

    action = ActionChains(ADT_LOGIN_PAGE.driver)
    # ADT_LOGIN_PAGE.driver.get("chrome://extensions/shortcuts") - cannot use this: raises element reference error
    edit_shortcut_shadow = selected_extension_card.find_element(By.CSS_SELECTOR, "extensions-shortcut-input")
    edit_shortcut_button = edit_shortcut_shadow.shadow_root.find_element(By.CSS_SELECTOR, "cr-icon-button#edit")
    edit_shortcut_button.click()
    # edit_shortcut_shadow.shadow_root.find_element(By.CSS_SELECTOR, "cr-input").shadow_root.find_element(By.CSS_SELECTOR, "#input").send_keys(Keys.COMMAND, 'i')
    edit_shortcut_shadow.shadow_root.find_element(By.CSS_SELECTOR, "cr-input").shadow_root.find_element(By.CSS_SELECTOR, "#input").click()
    action.key_down(Keys.COMMAND).send_keys('m').perform()
    action.move_to_element(ADT_LOGIN_PAGE.driver.find_element(By.TAG_NAME, 'body'))
    action.key_down(Keys.COMMAND).send_keys('m').perform()
    # pyautogui.hotkey('command', 'm')
    # print(edit_shortcut_shadow.shadow_root.find_element(By.CSS_SELECTOR, "cr-input").shadow_root.find_element(By.CSS_SELECTOR, "#error").text)

    set_adapter_url(extension_id)
    common.system_wait(2)
    for attempt in range(10):
        pyautogui.hotkey('command', 'm')
        if len(ADT_LOGIN_PAGE.driver.window_handles) > 1:
            common.switch_tabs(driver_=ADT_LOGIN_PAGE.driver, tab_id=ADT_LOGIN_PAGE.driver.window_handles[1])
            if ADT_LOGIN_PAGE.driver.title == 'Adapter':
                break

    # set shortcut
    pyautogui.hotkey('altleft', 'i')
    ADT_LOGIN_PAGE.open_page()
    element = ADT_LOGIN_PAGE.driver.find_element(By.XPATH, "//*[@id='username']")
    ADT_LOGIN_PAGE.driver.find_element(By.XPATH, "//*").send_keys(Keys.CONTROL+Keys.SHIFT+"a")
    common.wait_page_element_load(ADT_LOGIN_PAGE.driver, login_steps.LOGIN_PAGE.user_input)
