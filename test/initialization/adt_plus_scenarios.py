import driver
from step_definitions import common_steps, script_steps, call_interaction_steps
from step_definitions.adapters import adapter_login_steps, adapter_steps, adapter_worksheet_steps
from test.initialization import base_setup


def check_adt_basic_calls():
    base_setup.set_base_pages(instances=2)
    common_steps.STARTED_PAGES.append(adapter_login_steps.ADAPTER_LOGIN_PAGE)
    common_steps.STARTED_PAGES.append(script_steps.SCRIPT_PAGE)
    common_steps.STARTED_PAGES.append(adapter_steps.ADAPTER_PAGE)
    common_steps.STARTED_PAGES.append(adapter_worksheet_steps.ADAPTER_WORKSHEET_PAGE)
    common_steps.STARTED_PAGES.append(call_interaction_steps.CALL_INTERACTION_PAGE)

    # find the extension
    for _driver in driver.DRIVERS:
        driver_ = driver.DRIVERS.get(_driver).get('instance')
        common_steps.set_adapter_shortcut(driver_, adapter_login_steps.EXTENSION_NAME)
        common_steps.set_adapter_url(driver_, common_steps.set_adapter_shortcut(driver_, adapter_login_steps.EXTENSION_NAME, True), adapter_login_steps.ADAPTER_LOGIN_PAGE)

    adapter_login_steps.launch_adapter()
