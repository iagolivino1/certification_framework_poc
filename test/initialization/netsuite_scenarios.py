from common import *

import driver
from step_definitions import common_steps, script_steps, call_interaction_steps, sf_login_steps
from step_definitions.adapters import adapter_login_steps, adapter_steps, adapter_worksheet_steps
from test.initialization import base_setup


def check_netsuite_basic_calls():
    base_setup.set_base_pages(instances=2)
    common_steps.STARTED_PAGES.append(adapter_login_steps.ADAPTER_LOGIN_PAGE)
    common_steps.STARTED_PAGES.append(script_steps.SCRIPT_PAGE)
    common_steps.STARTED_PAGES.append(adapter_steps.ADAPTER_PAGE)
    common_steps.STARTED_PAGES.append(adapter_worksheet_steps.ADAPTER_WORKSHEET_PAGE)
    common_steps.STARTED_PAGES.append(call_interaction_steps.CALL_INTERACTION_PAGE)
    common_steps.STARTED_PAGES.append(sf_login_steps.LOGIN_PAGE)

    lab_config = f"configuration/lab/{get_config_file_section('config.yml', 'configuration').get('lab')}.yml"
    connector_url_ = get_config_file_section(lab_config, 'configuration').get('connector_url')
    if connector_url_:
        call_interaction_steps.CALL_INTERACTION_PAGE.connector_url = connector_url_

    try:
        sf_login_steps.AGENT_CREDENTIALS = get_config_file_section(lab_config, 'ns_credentials')
    except KeyError as e:
        print(f'could not find "credentials" section in {driver.CONFIG_FILE}.\n{e}\nusing the default...')
        sf_login_steps.AGENT_CREDENTIALS = get_config_file_section('config.yml', 'credentials')

    # find the extension
    for _driver in driver.DRIVERS:
        driver_ = driver.DRIVERS.get(_driver).get('instance')
        common_steps.set_adapter_shortcut(driver_, adapter_login_steps.NS_EXTENSION_NAME)
        common_steps.set_adapter_url(driver_, common_steps.set_adapter_shortcut(driver_, adapter_login_steps.NS_EXTENSION_NAME, True), adapter_login_steps.ADAPTER_LOGIN_PAGE, 'adapter_ns_login_url')
        break
