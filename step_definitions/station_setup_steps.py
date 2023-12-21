import common
from page_objects.station_setup_page import StationSetupPage
from pytest_bdd import (
    given,
    when
)

STATION_SETUP = None


def set_pages(driver):
    global STATION_SETUP
    STATION_SETUP = StationSetupPage(driver)


@when("I configure station with none option")
def configure_none_station(driver):
    set_pages(driver)
    common.wait_page_element_load(driver, STATION_SETUP.none_station, 120)
    STATION_SETUP.get_none_station_type().click()
    STATION_SETUP.get_next_button().click()
