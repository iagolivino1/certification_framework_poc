import common
from common import *
from step_definitions import login_steps, agent_steps, home_page_steps, common_steps, station_setup_steps


def set_base_pages(instances=1):
    common.TEST_INFO['lab'] = get_config_file_section('config.yml', 'configuration').get('lab').split('_')[0]
    common.TEST_INFO['platform'] = get_config_file_section('config.yml', 'configuration').get('platform_tool').split('_')[0]

    lab_config = f"configuration/lab/{get_config_file_section('config.yml', 'configuration').get('lab')}.yml"
    try:
        common_steps.AGENT_CREDENTIALS = get_config_file_section(lab_config, 'credentials')
    except KeyError as e:
        print(f'could not find "credentials" section in {driver.CONFIG_FILE}.\n{e}\nusing the default...')
        common_steps.AGENT_CREDENTIALS = get_config_file_section('config.yml', 'credentials')

    # set ready for field
    for agent in common_steps.AGENT_CREDENTIALS:
        common_steps.AGENT_CREDENTIALS.get(agent)['ready_channels'] = []

    # set login url if any
    login_url = get_config_file_section(lab_config, 'configuration').get('login_url')
    if login_url:
        login_steps.LOGIN_PAGE.url = login_url

    # set connector url if any
    connector_url_ = get_config_file_section(lab_config, 'configuration').get('connector_url')
    if connector_url_:
        common_steps.COMMON_PAGE.connector_url = connector_url_

    # start number of browser instances will be needed
    hub_url = get_config_file_section(f'{driver.CONFIG_FILE}', 'configuration').get('hub_url')
    for i in range(instances):
        driver.DRIVERS[f'{i}'] = {'instance': driver.new_driver(hub_url=hub_url), 'number_of_tabs': 1}

    # save started pages
    common_steps.STARTED_PAGES.append(login_steps.LOGIN_PAGE)
    common_steps.STARTED_PAGES.append(agent_steps.AGENT_HOME)
    common_steps.STARTED_PAGES.append(home_page_steps.HOME_PAGE)
    common_steps.STARTED_PAGES.append(common_steps.COMMON_PAGE)
    common_steps.STARTED_PAGES.append(station_setup_steps.STATION_SETUP)
    common_steps.set_current_browser('1')
