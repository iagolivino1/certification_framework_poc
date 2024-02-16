import importlib
import pytest

import driver
from step_definitions import common_steps

pytest_plugins = [
   "step_definitions.agent_steps",
   "step_definitions.chat_template_steps",
   "step_definitions.common_steps",
   "step_definitions.home_page_steps",
   "step_definitions.login_steps",
   "step_definitions.station_setup_steps"
]


def pytest_bdd_before_scenario(request, feature, scenario):
    print('setting up browser instances and pages...')
    scenario_location_split = scenario.feature.filename.split("/")
    scenario_file_name = scenario_location_split[len(scenario_location_split)-1]
    setup_module = importlib.import_module(f"test.initialization.{scenario_file_name.replace('.feature', '')}")
    setup_function = scenario.name.lower().replace(" ", "_")
    getattr(setup_module, setup_function)()
    print('browser instances and pages set!')


@pytest.fixture
def start_message():
    return "Automatic Message"


@pytest.fixture
def reply_message():
    return "Automatic Reply"


def pytest_bdd_after_scenario(request, feature, scenario):
    print('reset variables...')
    common_steps.reset_variables()
    print('variables reset!')
    print('closing all existent browser instances...')
    open_browsers = len(driver.DRIVERS)
    for d in range(open_browsers):
        d_ = driver.DRIVERS[d-1]
        driver.DRIVERS.remove(d_)
        d_.quit()
    print('browser instances closed!')
