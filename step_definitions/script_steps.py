import common
from pytest_bdd import when
from selenium.webdriver.common.by import By
from page_objects.script_page import ScriptPage
from step_definitions.adapters import adt_adapter_steps

SCRIPT_PAGE = ScriptPage()


@when("I check the call script window")
def check_call_script_window():
    assert 'Five9 Adapter - Script' in SCRIPT_PAGE.driver.title, "SCRIPT WINDOW DID NOT OPEN PROPERLY"
    common.wait_page_element_load(SCRIPT_PAGE.driver, SCRIPT_PAGE.script_content)
    common.switch_to_frame(SCRIPT_PAGE.driver, SCRIPT_PAGE.get_script_content())
    common.wait_page_element_load(SCRIPT_PAGE.driver, SCRIPT_PAGE.header)
    assert "Inbound Call Arriving!" in SCRIPT_PAGE.get_header().text, "SCRIPT HEADER DID NOT LOAD PROPERLY"
    assert adt_adapter_steps.CALL_NUMBER in SCRIPT_PAGE.get_phone_number().text, "CUSTOMER PHONE NUMBER DID NOT LOAD PROPERLY"
