import importlib
import pytest
import driver
import common
from step_definitions import common_steps


pytest_plugins = [
   "step_definitions.agent_steps",
   "step_definitions.chat_template_steps",
   "step_definitions.common_steps",
   "step_definitions.home_page_steps",
   "step_definitions.login_steps",
   "step_definitions.script_steps",
   "step_definitions.station_setup_steps",
   "step_definitions.call_interaction_steps",
   "step_definitions.adapters.adt_login_steps",
   "step_definitions.adapters.adt_adapter_steps",
   "step_definitions.adapters.adt_worksheet_steps"
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
        d_ = driver.DRIVERS.get(str(d)).get('instance')
        driver.DRIVERS.pop(str(d))
        d_.quit()
    print('browser instances closed!')


def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    print(f"starting step: {step}")


def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    # update browser tab title
    # common_page will always be started
    # driver.DRIVERS.index(common_steps.COMMON_PAGE.driver)
    tab_info = {'title': common_steps.COMMON_PAGE.driver.title, 'browser_number': int(common.get_driver_by_instance(common_steps.COMMON_PAGE.driver))}
    common.BROWSER_TABS[common_steps.COMMON_PAGE.driver.current_window_handle] = tab_info
    print(f"step finished!")
