import configparser
import os
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_configuration_file(file_name):
    config = configparser.RawConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + os.sep + file_name.replace("../", ""))
    return config


def get_config_file_section(file_name, section):
    return dict(read_configuration_file(file_name).items(section))


def wait_page_element_load(driver, element_xpath, timeout_in_seconds=30):
    WebDriverWait(driver, timeout_in_seconds).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))


def wait_element_to_be_clickable(driver, element_xpath, timeout_in_seconds=30):
    WebDriverWait(driver, timeout_in_seconds).until(EC.element_to_be_clickable((By.XPATH, element_xpath)))


def wait_element_to_be_selected(driver, element, timeout_in_seconds=30):
    WebDriverWait(driver, timeout_in_seconds).until(EC.element_to_be_selected(element))


def switch_tabs(driver, tab=None):
    """
    only use this method without @tab when you are working with 2 tabs
    for more than 2 tabs you should always pass the @tab name
    """
    if tab:
        driver.switch_to.window(tab)
    else:
        current_window = driver.current_window_handle
        for window in driver.window_handles:
            if window != current_window:
                driver.switch_to.window(window)


def switch_to_frame(driver, frame):
    driver.switch_to.frame(frame)


def click_element(driver, element):
    driver.execute_script("arguments[0].click();", element)


def wait_page_to_be(driver, url):
    WebDriverWait(driver, 60).until(EC.url_contains(url))


def assert_condition(condition, message):
    try:
        assert condition, message
    except AssertionError as e:
        print(f'{message}: \nerror: {e}')


def wait_element_class_contains(driver, element_xpath, text, timeout_in_seconds=30):
    WebDriverWait(driver, timeout_in_seconds).until(
        EC.text_to_be_present_in_element_attribute((By.XPATH, element_xpath), "class", text))


def _wait_elements_number_to_be(driver, element_xpath, element_number, more_than=True, timeout_in_seconds=60):
    start_time = 0
    while start_time < timeout_in_seconds:
        elements = len(driver.find_elements(By.XPATH, element_xpath))
        if more_than:
            if elements > element_number:
                return True
        else:
            if elements < element_number:
                return True
        sleep(1)
        start_time += 1
    raise Exception(f'Element number should be {element_number} but it is {len(driver.find_elements(By.XPATH, element_xpath))}.')


def wait_element_to_be_more_than(driver, element_xpath, element_number, timeout_in_seconds=60):
    return _wait_elements_number_to_be(driver, element_xpath, element_number, timeout_in_seconds=timeout_in_seconds)


def wait_elements_to_be_less_than(driver, element_xpath, element_number, timeout_in_seconds=60):
    return _wait_elements_number_to_be(driver, element_xpath, element_number, more_than=False, timeout_in_seconds=timeout_in_seconds)


def move_to_and_click_element(driver, element_xpath):
    action = ActionChains(driver)
    action.move_to_element(driver.find_element(By.XPATH, element_xpath)).click().perform()


def set_focus_out_element(driver, element):
    driver.execute_script("arguments[0].blur();", element)


def element_recursive_click(driver, element_xpath, click_times=1):
    for i in range(click_times):
        driver.find_element(By.XPATH, element_xpath).click()
        sleep(0.5)


def system_wait(time_to_wait=1):
    sleep(time_to_wait)
