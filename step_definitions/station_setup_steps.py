import common
from page_objects.station_setup_page import StationSetupPage
from pytest_bdd import (
    given,
    when
)

STATION_SETUP = StationSetupPage()


@when("I configure station with none option")
def configure_none_station():
    common.wait_page_element_load(STATION_SETUP.driver, STATION_SETUP.none_station, 120)
    STATION_SETUP.get_none_station_type().click()
    STATION_SETUP.get_next_button().click()
