from common import *
from step_definitions import call_interaction_steps, common_steps, sf_login_steps, sf_home_page_steps, sf_agent_steps
from test.initialization import base_setup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def check_sf_basic_calls():
    base_setup.set_base_pages(1)
    common_steps.STARTED_PAGES.append(sf_login_steps.LOGIN_PAGE)
    common_steps.STARTED_PAGES.append(sf_home_page_steps.HOME_PAGE)
    common_steps.STARTED_PAGES.append(sf_agent_steps.SF_AGENT_HOME)

    # set connector url if any
    lab_config = f"configuration/lab/{get_config_file_section('config.yml', 'configuration').get('lab')}.yml"
    connector_url_ = get_config_file_section(lab_config, 'configuration').get('connector_url')
    if connector_url_:
        call_interaction_steps.CALL_INTERACTIONS.connector_url = connector_url_

    try:
        sf_login_steps.AGENT_CREDENTIALS = get_config_file_section(lab_config, 'sf_credentials')
    except KeyError as e:
        print(f'could not find "credentials" section in {driver.CONFIG_FILE}.\n{e}\nusing the default...')
        sf_login_steps.AGENT_CREDENTIALS = get_config_file_section('config.yml', 'credentials')
