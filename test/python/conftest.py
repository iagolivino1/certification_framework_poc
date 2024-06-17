import importlib
import pytest
import driver
import common
import allure
from step_definitions import common_steps, login_steps

pytest_plugins = [
   "step_definitions.agent_steps",
   "step_definitions.chat_template_steps",
   "step_definitions.chat_interaction_steps",
   "step_definitions.common_steps",
   "step_definitions.home_page_steps",
   "step_definitions.login_steps",
   "step_definitions.script_steps",
   "step_definitions.station_setup_steps",
   "step_definitions.call_interaction_steps",
   "step_definitions.adapters.adapter_login_steps",
   "step_definitions.adapters.adapter_steps",
   "step_definitions.adapters.adapter_worksheet_steps",
   "step_definitions.sf_login_steps"
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
    print('checking if any agent is logged in...')
    if request.node.__scenario_report__.current_step_report.failed:
        login_steps.perform_logout()
    print('logged agent check done!')
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

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    open_browsers = len(driver.DRIVERS)
    for d in range(open_browsers):
        d_ = driver.DRIVERS.get(str(d)).get('instance')
        allure.attach(d_.get_screenshot_as_png(), name=d_.title, attachment_type=allure.attachment_type.PNG)