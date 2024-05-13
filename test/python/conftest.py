import importlib
import pytest
import driver
import re
from step_definitions import common_steps
from typing import List
from pathlib import Path


pytest_plugins = [
   "step_definitions.agent_steps",
   "step_definitions.chat_template_steps",
   "step_definitions.common_steps",
   "step_definitions.home_page_steps",
   "step_definitions.login_steps",
   "step_definitions.station_setup_steps",
   "step_definitions.call_interaction_steps"
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


# code from https://stackoverflow.com/questions/72295235/pytest-bdd-single-scenario-outline-multiple-examples
# the intention of this code is to make the example table tags findable
'''def pytest_collection_modifyitems(items: List[pytest.Item]):
    for item in items:
        if not hasattr(item, "_pyfuncitem") or not hasattr(item, "callspec"):
            continue
        feature = item._pyfuncitem._obj.__scenario__.feature
        feature_content_lines = Path(feature.filename).read_text().splitlines()
        parameters = list(item.callspec.params["_pytest_bdd_example"].values())
        examples_start_line = None
        for i, line in enumerate(feature_content_lines):
            if "Examples:" in line:
                examples_start_line = i
                continue
            elif re.match(r"[|\s]+{}[|\s]+".format(r"[|\s]+".join(parameters)), line):
                break
        if examples_start_line is None:
            continue
        tag_match = re.search(
            r"@(?P<tag>\S+)", feature_content_lines[examples_start_line - 1]
        )
        if tag_match is None:
            continue
        tag = tag_match.group("tag")
        item.add_marker(tag)'''
