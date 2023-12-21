import common
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


class Driver(object):
    def __init__(self, hub, instance_counter=1):
        # platform options: https://saucelabs.com/products/platform-configurator
        self.instance_counter = instance_counter
        self.hub = hub
        self.configuration = common.get_config_file_section('config.ini', 'configuration')
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
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-notifications')

        func = getattr(self, "_"+browser.replace("-", "_"))
        return func(options)

    def _sauce_options(self):
        sauce_options = {'username': self.configuration.get('username'),
                         'accessKey': self.configuration.get('access_key'),
                         'build': self.configuration.get('build')if self.instance_counter == 1 else self.configuration.get('build2'),
                         'name': self.configuration.get('test_name')}
        return sauce_options

    def _remote(self, options):
        options.browser_version = self.configuration.get('browser_version')
        options.platform_name = self.configuration.get('platform')
        options.set_capability('sauce:options', self._sauce_options())
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
