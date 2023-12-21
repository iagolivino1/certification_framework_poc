import pytest
from driver import Driver
import common

pytest_plugins = [
   "step_definitions.agent_steps",
   "step_definitions.chat_template_steps",
   "step_definitions.common_steps",
   "step_definitions.home_page_steps",
   "step_definitions.login_steps",
   "step_definitions.station_setup_steps"
]


# create driver as fixture to be used in the test scripts
@pytest.fixture
def driver():
    hub_url = common.get_config_file_section('config.ini', 'configuration').get('hub_url')
    driver = Driver(hub=hub_url).driver
    yield driver
    driver.quit()


@pytest.fixture
def driver2():
    # getting error:
    # response = {'status': 500, 'value': '{"status": 13, "sessionId": "9b8e6a41060f46768947ebdbdf2fbaed", "value": {"message": "Job no...nization has reached its concurrent session limit.\\nContact your administrator or sales@saucelabs.com to upgrade."}}'}
    hub_url = common.get_config_file_section('config.ini', 'configuration').get('hub_url')
    driver = Driver(hub=hub_url, instance_counter=2).driver
    yield driver
    driver.quit()


@pytest.fixture
def start_message():
    return "Automatic Message"


@pytest.fixture
def reply_message():
    return "Automatic Reply"
