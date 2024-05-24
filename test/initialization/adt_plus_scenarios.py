import pyautogui
import common
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from step_definitions import common_steps, script_steps, call_interaction_steps
from step_definitions.adapters import adapter_login_steps, adapter_steps, adapter_worksheet_steps
from test.initialization import base_setup


def check_adt_basic_calls():
    base_setup.set_base_pages(instances=2)
    common_steps.STARTED_PAGES.append(adapter_login_steps.ADAPTER_LOGIN_PAGE)
    common_steps.STARTED_PAGES.append(script_steps.SCRIPT_PAGE)
    common_steps.STARTED_PAGES.append(adapter_steps.ADAPTER_PAGE)
    common_steps.STARTED_PAGES.append(adapter_worksheet_steps.ADAPTER_WORKSHEET_PAGE)
    common_steps.STARTED_PAGES.append(call_interaction_steps.CALL_INTERACTION_PAGE)

    # find the extension
    set_adapter_shortcut(adapter_login_steps.EXTENSION_NAME)
    set_adapter_url(set_adapter_shortcut(adapter_login_steps.EXTENSION_NAME, True))

    # open the adapter window
    for attempt in range(10):
        common.wait_element_to_be_clickable(common_steps.COMMON_PAGE.driver, "//body")
        common.click_element(common_steps.COMMON_PAGE.driver, common_steps.COMMON_PAGE.driver.find_element(By.TAG_NAME, "body"))
        pyautogui.hotkey(
            adapter_login_steps.PLATFORM_HOTKEYS.get(common_steps.COMMON_PAGE.driver.caps.get('platformName'))[1], 'i')
        common.system_wait(2)
        if len(common_steps.COMMON_PAGE.driver.window_handles) > 1:
            common.switch_tabs(driver_=common_steps.COMMON_PAGE.driver, tab_id=common_steps.COMMON_PAGE.driver.window_handles[1])
            if common_steps.COMMON_PAGE.driver.title != 'Adapter':
                common.wait_page_element_load(common_steps.COMMON_PAGE.driver, "//*[@id='username']", 60)
                break


# ----- SETUP ----- #
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
    action.key_down(adapter_login_steps.PLATFORM_HOTKEYS.get(common_steps.COMMON_PAGE.driver.caps.get('platformName'))[0])\
        .send_keys('i')\
        .key_up(adapter_login_steps.PLATFORM_HOTKEYS.get(common_steps.COMMON_PAGE.driver.caps.get('platformName'))[0])\
        .perform()


def set_adapter_url(extension_id):
    lab_config = f"configuration/lab/{common.get_config_file_section('config.yml', 'configuration').get('lab')}.yml"
    adapter_url = common.get_config_file_section(lab_config, 'configuration').get('adapter_login_url')
    if not adapter_url:
        adapter_url = adapter_login_steps.ADAPTER_LOGIN_PAGE.url
    adapter_login_steps.ADAPTER_LOGIN_PAGE.url = adapter_url
    common_steps.COMMON_PAGE.driver.get(f"chrome-extension://{extension_id}/options.html")
    common.system_wait(2)

    # set extension url
    input_url = common_steps.COMMON_PAGE.driver.find_element(By.XPATH, "//input[@id='url']")
    input_url.clear()
    input_url.click()
    input_url.send_keys(adapter_url)
    try:
        assert input_url.get_attribute('value') == adapter_url
    except AssertionError:
        input_url.clear()
        input_url.send_keys(adapter_url)
        assert input_url.get_attribute('value') == adapter_url, "COULD NOT SET THE CORRECT URL"
    common_steps.COMMON_PAGE.driver.find_element(By.XPATH, "//button[@id='save']").click()
    common.wait_element_attribute_contains(common_steps.COMMON_PAGE.driver, "//mark[@id='status']", 'innerText', "Options Saved")
    tab_info = {'title': common_steps.COMMON_PAGE.driver.title,
                'browser_number': int(common.get_driver_by_instance(common_steps.COMMON_PAGE.driver))}
    common.BROWSER_TABS[common_steps.COMMON_PAGE.driver.current_window_handle] = tab_info