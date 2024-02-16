from configparser import NoSectionError
import driver
from common import *
from step_definitions import login_steps, agent_steps, home_page_steps, common_steps, station_setup_steps


def set_base_pages(instances=1):
    try:
        login_steps.CREDENTIALS = get_config_file_section(f'{driver.CONFIG_FILE}', 'credentials')
    except NoSectionError as e:
        print(f'could not find "credentials" section in {driver.CONFIG_FILE}.\n{e}\nusing the default...')
        login_steps.CREDENTIALS = get_config_file_section('config.ini', 'credentials')

    # start number of browser instances will be needed
    hub_url = get_config_file_section(f'{driver.CONFIG_FILE}', 'configuration').get('hub_url')
    for i in range(instances):
        driver.DRIVERS.append(driver.new_driver(hub_url=hub_url))

    login_steps.LOGIN_PAGE.driver = driver.DRIVERS[0]
    agent_steps.AGENT_HOME.driver = driver.DRIVERS[0]
    home_page_steps.HOME_PAGE.driver = driver.DRIVERS[0]
    common_steps.COMMON_PAGE.driver = driver.DRIVERS[0]
    station_setup_steps.STATION_SETUP.driver = driver.DRIVERS[0]
