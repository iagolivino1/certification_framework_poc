import common
from page_objects.station_setup_page import StationSetupPage
from pytest_bdd import when, parsers
from step_definitions import common_steps

STATION_SETUP = StationSetupPage()


@when(parsers.parse("I select {station_type} for station type"))
def select_station_type(station_type):
    common_steps.wait_modal_dialog_open('station', 300)
    common.wait_page_element_load(STATION_SETUP.driver, STATION_SETUP.none_station, 120)
    if station_type == 'None':
        STATION_SETUP.get_none_station_type().click()
    elif station_type == 'Softphone':
        STATION_SETUP.get_softphone_station_type().click()
    elif station_type == 'WebRTC':
        STATION_SETUP.get_webrtc_station_type().click()
    elif station_type == 'Gateway':
        STATION_SETUP.get_gateway_station_type().click()
    else:
        raise Exception('station type not valid!')


@when(parsers.parse("I configure station with {id_} id"))
def configure_station_id(id_):
    for input_ in STATION_SETUP.get_station_input():
        if input_.is_displayed():
            input_.clear()
            input_.send_keys(id_)
            break
    common_steps.select_modal_next_button()
    common_steps.wait_modal_dialog_open('station_check', 30)
    common.wait_element_to_be_clickable(STATION_SETUP.driver, STATION_SETUP.station_tone_check_status, 60)
    assert STATION_SETUP.get_station_tone_check_status().text == "Connection Successful"
    common.wait_element_to_be_clickable(STATION_SETUP.driver, STATION_SETUP.restart_station_button, 60)
