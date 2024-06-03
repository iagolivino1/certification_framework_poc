import pyautogui
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import common
from step_definitions import common_steps, script_steps
from step_definitions.adapters import adt_login_steps, adt_adapter_steps, adt_worksheet_steps
from test.initialization import base_setup


def login_adt():
    base_setup.set_base_pages()
    common_steps.STARTED_PAGES.append(adt_login_steps.ADT_LOGIN_PAGE)
    common_steps.STARTED_PAGES.append(script_steps.SCRIPT_PAGE)
    common_steps.STARTED_PAGES.append(adt_adapter_steps.ADT_ADAPTER_PAGE)
    common_steps.STARTED_PAGES.append(adt_worksheet_steps.ADT_WORKSHEET_PAGE)

    # find the extension
    set_adapter_shortcut(adt_login_steps.EXTENSION_NAME)
    set_adapter_url(set_adapter_shortcut(adt_login_steps.EXTENSION_NAME, True))

    # open the adapter window
    for attempt in range(10):
        common_steps.COMMON_PAGE.driver.find_element(By.TAG_NAME, "body").click()
        pyautogui.hotkey(
            adt_login_steps.PLATFORM_HOTKEYS.get(common_steps.COMMON_PAGE.driver.caps.get('platformName'))[1], 'i')
        common.system_wait(6)
        if len(common_steps.COMMON_PAGE.driver.window_handles) > 1:
            common.switch_tabs(driver_=common_steps.COMMON_PAGE.driver, tab_id=common_steps.COMMON_PAGE.driver.window_handles[1])
            if common_steps.COMMON_PAGE.driver.title != 'Adapter':
                common.wait_page_element_load(common_steps.COMMON_PAGE.driver, "//*[@id='username']", 60)
                break


def set_adapter_shortcut(extension_text, return_id=False):
    common_steps.COMMON_PAGE.driver.get("chrome://extensions")
    extension_manager_element_shadow = common_steps.COMMON_PAGE.driver.find_element(By.XPATH, "//extensions-manager")
    extension_items_list_shadow = extension_manager_element_shadow.shadow_root.find_element(By.CSS_SELECTOR,
                                                                                            "#items-list")
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
    common.wait_page_to_be(common_steps.COMMON_PAGE.driver, "?id=")
    if return_id:
        return common_steps.COMMON_PAGE.driver.current_url.split("?id=")[1].strip()

    left_panel_shadow = extension_manager_element_shadow.shadow_root.find_element(By.CSS_SELECTOR, "extensions-sidebar")
    keyboard_shortcuts = left_panel_shadow.shadow_root.find_element(By.CSS_SELECTOR, "a#sectionsShortcuts")
    keyboard_shortcuts.click()

    keyboard_shortcuts_content_shadow = extension_manager_element_shadow.shadow_root.find_element(By.CSS_SELECTOR,
                                                                                                  "extensions-keyboard-shortcuts")
    extension_cards = keyboard_shortcuts_content_shadow.shadow_root.find_elements(By.CSS_SELECTOR, ".shortcut-card")
    selected_extension_card = None
    for extension_card in extension_cards:
        if extension_text in extension_card.text:
            selected_extension_card = extension_card
            break
    if not selected_extension_card:
        raise Exception(f"card for {extension_text} extension not found")

    action = ActionChains(common_steps.COMMON_PAGE.driver)
    edit_shortcut_shadow = selected_extension_card.find_element(By.CSS_SELECTOR, "extensions-shortcut-input")
    edit_shortcut_button = edit_shortcut_shadow.shadow_root.find_element(By.CSS_SELECTOR, "cr-icon-button#edit")
    edit_shortcut_button.click()
    edit_shortcut_shadow.shadow_root.find_element(By.CSS_SELECTOR, "cr-input").shadow_root.find_element(By.CSS_SELECTOR, "#input").click()
    action.key_down(adt_login_steps.PLATFORM_HOTKEYS.get(common_steps.COMMON_PAGE.driver.caps.get('platformName'))[0])\
        .send_keys('i')\
        .key_up(adt_login_steps.PLATFORM_HOTKEYS.get(common_steps.COMMON_PAGE.driver.caps.get('platformName'))[0])\
        .perform()


def set_adapter_url(extension_id):
    common_steps.COMMON_PAGE.driver.get(f"chrome-extension://{extension_id}/options.html")
    common.system_wait(2)

    # set extension url
    input_url = common_steps.COMMON_PAGE.driver.find_element(By.XPATH, "//input[@id='url']")
    input_url.clear()
    input_url.click()
    input_url.send_keys(adt_login_steps.ADT_LOGIN_PAGE.url)
    try:
        assert input_url.get_attribute('value') == adt_login_steps.ADT_LOGIN_PAGE.url
    except AssertionError:
        input_url.clear()
        input_url.send_keys(adt_login_steps.ADT_LOGIN_PAGE.url)
        assert input_url.get_attribute('value') == adt_login_steps.ADT_LOGIN_PAGE.url, "COULD NOT SET THE CORRECT URL"
    common_steps.COMMON_PAGE.driver.find_element(By.XPATH, "//button[@id='save']").click()
    common.wait_element_attribute_contains(common_steps.COMMON_PAGE.driver, "//mark[@id='status']", 'innerText', "Options Saved")
    tab_info = {'title': common_steps.COMMON_PAGE.driver.title,
                'browser_number': int(common.get_driver_by_instance(common_steps.COMMON_PAGE.driver))}
    common.BROWSER_TABS[common_steps.COMMON_PAGE.driver.current_window_handle] = tab_info
