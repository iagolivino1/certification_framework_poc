import common
from common import *
from step_definitions import call_interaction_steps, common_steps, sf_login_steps, script_steps
from step_definitions.adapters import adapter_login_steps, adapter_steps, adapter_worksheet_steps
from test.initialization import base_setup


def check_sf_basic_calls():
    base_setup.set_base_pages(2)
    common_steps.STARTED_PAGES.append(sf_login_steps.LOGIN_PAGE)
    common_steps.STARTED_PAGES.append(call_interaction_steps.CALL_INTERACTION_PAGE)
    common_steps.STARTED_PAGES.append(adapter_login_steps.ADAPTER_LOGIN_PAGE)
    common_steps.STARTED_PAGES.append(adapter_steps.ADAPTER_PAGE)
    common_steps.STARTED_PAGES.append(script_steps.SCRIPT_PAGE)
    common_steps.STARTED_PAGES.append(adapter_worksheet_steps.ADAPTER_WORKSHEET_PAGE)

    # set connector url if any
    lab_config = f"configuration/lab/{get_config_file_section('config.yml', 'configuration').get('lab')}.yml"
    connector_url_ = get_config_file_section(lab_config, 'configuration').get('connector_url')
    if connector_url_:
        call_interaction_steps.CALL_INTERACTION_PAGE.connector_url = connector_url_

    try:
        sf_login_steps.AGENT_CREDENTIALS = get_config_file_section(lab_config, 'sf_credentials')
    except KeyError as e:
        common.LOGGER.warning(message=f'could not find "credentials" section in {driver.CONFIG_FILE}.\n{e}\nusing the default...')
        sf_login_steps.AGENT_CREDENTIALS = get_config_file_section('config.yml', 'credentials')
        common.LOGGER.info(message=f"sf agent credentials: {sf_login_steps.AGENT_CREDENTIALS}")
