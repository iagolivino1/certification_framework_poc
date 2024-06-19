import datetime
import importlib
import os
import sys
import pytest
import driver
import common
import allure
import logging
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


# configure the logger before the test starts
def pytest_sessionstart(session):
    current_path = os.path.dirname(sys.executable.split('venv')[0]) + os.sep  # TODO: remove this temporary fix
    common.check_log_dir(current_path)
    log_file_path = f"{current_path}logs/log_{str(datetime.datetime.now()).replace(' ', '_').replace(':', '').split('.')[0]}.log"
    logging.basicConfig(level=logging.INFO, filename=log_file_path, filemode='w', format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', force=True)
    common.LOGGER.set_logger(logging.getLogger())
    common.LOGGER.info(message=f'setting log configs')
    common.LOGGER.info(message=f'path: {current_path}')
    common.LOGGER.info(message=f'log file: {log_file_path}')


def pytest_bdd_before_scenario(request, feature, scenario):
    common.LOGGER.system('log file configuration created!')
    common.LOGGER.info(message=f'starting scenario: {scenario.name}')
    common.LOGGER.system('setting up browser instances and pages...')
    scenario_location_split = scenario.feature.filename.split("/")
    scenario_file_name = scenario_location_split[len(scenario_location_split)-1]
    setup_module = importlib.import_module(f"test.initialization.{scenario_file_name.replace('.feature', '')}")
    setup_function = scenario.name.lower().replace(" ", "_")
    getattr(setup_module, setup_function)()
    common.LOGGER.system(message=f"started pages: {common_steps.STARTED_PAGES}")
    common.LOGGER.system('browser instances and pages set!')
    common.LOGGER.info(message='test started...')


@pytest.fixture
def start_message():
    return "Automatic Message"


@pytest.fixture
def reply_message():
    return "Automatic Reply"


def pytest_bdd_after_scenario(request, feature, scenario):
    common.LOGGER.system('reset variables...')
    common_steps.reset_variables()
    common.LOGGER.system('variables reset!')
    common.LOGGER.info(message='checking if any agent is logged in...')
    if request.node.__scenario_report__.current_step_report.failed:
        login_steps.perform_logout()
    common.LOGGER.info(message='logged agent check done!')
    common.LOGGER.system('closing all existent browser instances...')
    open_browsers = len(driver.DRIVERS)
    for d in range(open_browsers):
        d_ = driver.DRIVERS.get(str(d)).get('instance')
        driver.DRIVERS.pop(str(d))
        d_.quit()
    common.LOGGER.system('browser instances closed!')


def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    common.LOGGER.info(message=f"starting step: {step}")
    common.LOGGER.agent(agent=common_steps.get_agent_for_logs(),
                        message=f'executing step: {step} | function: {step_func} | with args: {step_func_args}')


def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    # update browser tab title
    # common_page will always be started
    tab_info = {'title': common_steps.COMMON_PAGE.driver.title, 'browser_number': int(common.get_driver_by_instance(common_steps.COMMON_PAGE.driver))}
    common.BROWSER_TABS[common_steps.COMMON_PAGE.driver.current_window_handle] = tab_info
    common.LOGGER.system(f'tab info saved: {tab_info}')
    common.LOGGER.agent(agent=common_steps.get_agent_for_logs(), message=f"finish step: {step}")


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    common.LOGGER.error(agent=common_steps.get_agent_for_logs(),
                        message=f'step failed: {step} | exception: {exception}')
    open_browsers = len(driver.DRIVERS)
    for d in range(open_browsers):
        d_ = driver.DRIVERS.get(str(d)).get('instance')
        allure.attach(d_.get_screenshot_as_png(), name=d_.title, attachment_type=allure.attachment_type.PNG)
