import os
import common
from configparser import NoSectionError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def new_driver(hub_url):
    driver_ = Driver(hub_url).driver
    driver_.maximize_window()
    return driver_


def __set_config_file():
    configuration = common.get_config_file_section('config.yml', 'configuration')
    return f'configuration/{configuration.get("platform_tool")}.yml'


DRIVERS = {}
CONFIG_FILE = __set_config_file()


class Driver(object):
    def __init__(self, hub, instance_counter=1):
        self.instance_counter = instance_counter
        self.hub = hub
        self.general_flags = common.get_config_file_section('config.yml', 'flags')
        self.configuration = common.get_config_file_section(CONFIG_FILE, 'configuration')
        self.driver = self._browser_options(self.configuration.get('browser'))

    def _browser_options(self, browser=None):
        if 'safari' in browser:
            options = SafariOptions()
        elif 'firefox' in browser:
            options = FirefoxOptions()
        elif 'edge' in browser:
            options = EdgeOptions()
        else:
            options = ChromeOptions()

        for general_flag in self.general_flags.values():
            options.add_argument(general_flag)

        try:
            browser_flags = common.get_config_file_section(CONFIG_FILE, f'{browser.split("-")[0]}_flags')
        except NoSectionError:
            browser_flags = {}

        try:
            browser_extensions = common.get_config_file_section(CONFIG_FILE, f'{browser.split("-")[0]}_extensions')
        except NoSectionError:
            browser_extensions = {}

        for browser_flag in browser_flags.values():
            options.add_argument(browser_flag)

        for browser_extension in browser_extensions.values():
            options.add_extension(os.path.dirname(os.path.realpath(__file__)) + os.sep + f'extensions/{browser_extension}')

        func = getattr(self, "_"+browser.replace("-", "_"))
        return func(options)

    def _bs_options(self):
        bstack_options = {
            "os": self.configuration.get('platform'),
            "osVersion": self.configuration.get('platform_version'),
            "buildName": self.configuration.get('build'),
            "sessionName": self.configuration.get('test_name'),
            "userName": self.configuration.get('username'),
            "accessKey": self.configuration.get('access_key')
        }
        return bstack_options

    def _sauce_options(self):
        sauce_options = {'username': self.configuration.get('username'),
                         'accessKey': self.configuration.get('access_key'),
                         'build': self.configuration.get('build'),
                         'name': self.configuration.get('test_name')}
        return sauce_options

    def _remote(self, options):
        tool_options = 'bstack:options', self._bs_options()
        options.browser_version = self.configuration.get('browser_version')
        if 'saucelabs' in CONFIG_FILE:
            options.platform_name = self.configuration.get('platform')
            tool_options = 'sauce:options', self._sauce_options()
        options.set_capability(tool_options[0], tool_options[1])
        return webdriver.Remote(command_executor=self.hub, options=options)

    def _chrome_remote(self, options):
        return self._remote(options)

    def _chrome_local(self, options):
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def _firefox_remote(self, options):
        return self._remote(options)

    def _firefox_local(self, options):
        return webdriver.Chrome(service=FirefoxService(GeckoDriverManager().install()), options=options)

    def _safari_remote(self, options):
        return self._remote(options)

    def _safari_local(self, options):
        return webdriver.Safari(options=options)

    def _edge_remote(self, options):
        return self._remote(options)

    def _edge_local(self, options):
        return webdriver.Chrome(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
