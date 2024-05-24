from common import *
from step_definitions import login_steps, agent_steps, home_page_steps, common_steps, station_setup_steps


def set_base_pages(instances=1):
    lab_config = f"configuration/lab/{get_config_file_section('config.yml', 'configuration').get('lab')}.yml"
    try:
        login_steps.AGENT_CREDENTIALS = get_config_file_section(lab_config, 'credentials')
    except KeyError as e:
        print(f'could not find "credentials" section in {driver.CONFIG_FILE}.\n{e}\nusing the default...')
        login_steps.AGENT_CREDENTIALS = get_config_file_section('config.yml', 'credentials')

    # set login url if any
    login_url = get_config_file_section(lab_config, 'configuration').get('login_url')
    if login_url:
        login_steps.LOGIN_PAGE.url = login_url

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
