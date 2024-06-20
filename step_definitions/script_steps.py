import common
from pytest_bdd import when
from page_objects.script_page import ScriptPage
from step_definitions import common_steps
from step_definitions.adapters import adapter_steps

SCRIPT_PAGE = ScriptPage()


@when("I check the call script window")
def check_call_script_window():
    common.wait_page_element_load(SCRIPT_PAGE.driver, SCRIPT_PAGE.script_content)
    assert 'Five9 Adapter - Script' in SCRIPT_PAGE.driver.title, "SCRIPT WINDOW DID NOT OPEN PROPERLY"
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="script window opened")
    common.switch_to_frame(SCRIPT_PAGE.driver, SCRIPT_PAGE.get_script_content())
    common.wait_page_element_load(SCRIPT_PAGE.driver, SCRIPT_PAGE.header)
    assert "Inbound Call Arriving!" in SCRIPT_PAGE.get_header().text, "SCRIPT HEADER DID NOT LOAD PROPERLY"
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"script header loaded: {SCRIPT_PAGE.get_header().text}")
    assert adapter_steps.CALL_NUMBER in SCRIPT_PAGE.get_phone_number().text, "CUSTOMER PHONE NUMBER DID NOT LOAD PROPERLY"
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message=f"customer phone number loaded: {SCRIPT_PAGE.get_phone_number().text}")
