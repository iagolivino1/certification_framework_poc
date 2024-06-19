import os
import yaml
import driver
from time import sleep
from selenium.common import TimeoutException, NoSuchWindowException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class CommonLogger:
    def __init__(self):
        self.__logger = None
        self.message = ''

    def set_logger(self, logger):
        self.__logger = logger

    def system(self, message):
        self.__logger.warning(f'[SYSTEM] {message}')

    def agent(self, agent='None', message=None):
        self.__logger.info(f'[{str(agent).upper()}] {message}')

    def debug(self, agent=None, message=None):
        msg = f'[DEBUG] [{agent.upper()}] {message}' if agent else f'[DEBUG] {message}'
        self.__logger.debug(msg)

    def info(self, agent=None, message=None):
        msg = f'[INFO] [{agent.upper()}] {message}' if agent else f'[INFO] {message}'
        self.__logger.info(msg)

    def warning(self, agent=None, message=None):
        msg = f'[WARN] [{agent.upper()}] {message}' if agent else f'[WARN] {message}'
        self.__logger.warning(msg)

    def error(self, agent='', message=None):
        msg = f'[ERROR] [{agent.upper()}] {message}' if agent else f'[ERROR] {message}'
        self.__logger.error(msg)


def check_log_dir(path):
    if not os.path.isdir(path + 'logs/'):
        os.mkdir(path + 'logs/')


def read_configuration_file(file_name):
    file_ = open(os.path.dirname(os.path.realpath(__file__)) + os.sep + file_name.replace("../", ""), 'r')
    return yaml.safe_load(file_)


def get_config_file_section(file_name, section):
    return read_configuration_file(file_name)[section]


def get_driver_by_instance(instance, return_index=True):
    # to set new value in the driver dict, return_index must be False
    for d_ in driver.DRIVERS:
        driver_ = driver.DRIVERS.get(d_)
        if driver_.get('instance') == instance:
            if return_index:
                return d_
            return driver_
    raise Exception("INSTANCE NOT FOUND IN INITIATED DRIVERS!")


def wait_page_element_load(driver_, element_xpath, timeout_in_seconds=30):
    WebDriverWait(driver_, timeout_in_seconds).until(ec.visibility_of_element_located((By.XPATH, element_xpath)))


def wait_element_to_be_clickable(driver_, element_xpath, timeout_in_seconds=30):
    WebDriverWait(driver_, timeout_in_seconds).until(ec.element_to_be_clickable((By.XPATH, element_xpath)))


def wait_element_to_be_selected(driver_, element, timeout_in_seconds=30):
    WebDriverWait(driver_, timeout_in_seconds).until(ec.element_to_be_selected(element))


def get_tab_id_by_title(tab_list=None, tab_title=None):
    if not tab_list:
        tab_list = BROWSER_TABS
    for tab_ in tab_list:
        try:
            if tab_list.get(tab_).get('title') == tab_title:
                return tab_
        except AttributeError:
            print(f"{tab_}: tab info was lost. if it is not updated automatically please check the after steps hook.")
    raise Exception(f"TAB TITLE {tab_title} NOT FOUND IN ANY OPENED TAB!")


def switch_tabs(driver_, tab_id=None, tab_title=None):
    # make sure that the current window handle is selected
    # to avoid opening new tabs (some kind of script or even manually)
    # so driver gets confused and does not select/stay on the correct current tab
    try:
        driver_.switch_to.window(driver_.current_window_handle)
    except NoSuchWindowException:
        print('for some reason the current window/tab was already closed!')
        driver.DRIVERS.get(get_driver_by_instance(driver_))['number_of_tabs'] = len(
            driver_.window_handles)

    eligible_tabs = {}
    for tab_ in driver_.window_handles:
        eligible_tabs[tab_] = BROWSER_TABS.get(tab_)
    if tab_id:
        driver_.switch_to.window(tab_id)
    else:
        try:
            title_ = driver_.title
        except NoSuchWindowException:
            driver_.switch_to.window(driver_.window_handles[0])
            title_ = driver_.title
        if title_ != tab_title:
            driver_.switch_to.window(get_tab_id_by_title(tab_list=eligible_tabs, tab_title=tab_title))


def switch_to_frame(driver_, frame):
    driver_.switch_to.frame(frame)


def click_element(driver_, element=None, element_xpath=None):
    if element_xpath:
        element = driver_.find_element(By.XPATH, element_xpath)
    driver_.execute_script("arguments[0].click();", element)


def wait_page_to_be(driver_, url):
    WebDriverWait(driver_, 60).until(ec.url_contains(url))


def wait_page_to_be_loaded(driver_, timeout_in_seconds=30):
    for sec_ in range(timeout_in_seconds):
        if driver_.execute_script("return document.readyState") == 'complete':
            return True
        sleep(1)
    raise TimeoutError(f"PAGE NOT LOADED IN {timeout_in_seconds} SECONDS!")


def assert_condition(condition, message):
    try:
        assert condition, message
    except AssertionError as e:
        print(f'{message}: \nerror: {e}')


def wait_element_class_contains(driver_, element_xpath, text, timeout_in_seconds=30):
    return wait_element_attribute_contains(driver_, element_xpath, "class", text, timeout_in_seconds)


def wait_element_attribute_contains(driver_, element_xpath, attribute, text, timeout_in_seconds=30):
    WebDriverWait(driver_, timeout_in_seconds).until(
        ec.text_to_be_present_in_element_attribute((By.XPATH, element_xpath), attribute, text))


def wait_element_attribute_to_be_not_available(driver_, element_xpath, attribute, timeout_in_seconds=30):
    WebDriverWait(driver_, timeout_in_seconds).until_not(ec.element_attribute_to_include((By.XPATH, element_xpath), attribute))


def _wait_elements_number_to_be(driver_, element_xpath, element_number, more_than=True, timeout_in_seconds=60):
    start_time = 0
    while start_time <= timeout_in_seconds:
        elements = len(driver_.find_elements(By.XPATH, element_xpath))
        if more_than:
            if elements > element_number:
                return True
        else:
            if elements < element_number:
                return True
        sleep(1)
        start_time += 1
    message = f"ELEMENT NUMBER IS NOT LESS THAN {element_number}. WAIT TIME: {timeout_in_seconds} SECONDS."
    if more_than:
        message = message.replace('LESS', 'MORE')
    raise TimeoutException(message)


def wait_element_to_be_more_than(driver_, element_xpath, element_number, timeout_in_seconds=60):
    return _wait_elements_number_to_be(driver_, element_xpath, element_number, timeout_in_seconds=timeout_in_seconds)


def wait_elements_to_be_less_than(driver_, element_xpath, element_number, timeout_in_seconds=60):
    return _wait_elements_number_to_be(driver_, element_xpath, element_number, more_than=False, timeout_in_seconds=timeout_in_seconds)


def wait_element_to_not_be_displayed(driver_, element_xpath, timeout_in_seconds=60):
    WebDriverWait(driver_, timeout_in_seconds).until(
        ec.invisibility_of_element((By.XPATH, element_xpath)))


def wait_element_to_be_enabled(driver_, element_xpath, timeout_in_seconds=30):
    for time_ in range(timeout_in_seconds):
        try:
            if driver_.find_element(By.XPATH, element_xpath).is_enabled():
                return True
        except StaleElementReferenceException:
            pass
        system_wait(1)
    raise TimeoutException(f"ELEMENT WAS NOT ENABLED. WAIT TIME: {timeout_in_seconds}")


def get_shadow_root(driver_, element):
    return driver_.execute_script('return arguments[0].shadowRoot', element)


def move_to_and_click_element(driver_, element_xpath):
    action = ActionChains(driver_)
    action.move_to_element(driver_.find_element(By.XPATH, element_xpath)).click().perform()


def set_focus_out_element(driver_, element):
    driver_.execute_script("arguments[0].blur();", element)


def element_recursive_click(driver_, element_xpath, click_times=1):
    for i in range(click_times):
        driver_.find_element(By.XPATH, element_xpath).click()
        sleep(0.5)


def system_wait(time_to_wait=1):
    sleep(time_to_wait)


def check_window_is_open(driver_, window_name):
    for handle in driver_.window_handles:
        title = driver_.title
        if title.lower().__contains__(window_name):
            return True
        else:
            driver_.switch_to.window(handle)
    return False


def find_and_switch_to_frame(driver_, frame_name):
    iframes = driver_.find_elements(By.XPATH, "//iframe")
    
    if len(iframes) == 0:
        driver_.refresh()
        wait_page_to_be_loaded(driver_)
        iframes = driver_.find_elements(By.XPATH, "//iframe")

        if len(iframes) == 0:
            raise NoSuchElementException

    for index, iframe in enumerate(iframes):
        # print(iframe)
        if iframe.get_property("name") == frame_name:
            switch_to_frame(driver_, iframe)
            return


TEST_INFO = {}
BROWSER_TABS = {}
LOGGER = CommonLogger()
