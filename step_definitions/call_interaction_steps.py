from pytest_bdd import parsers, when

import common
from page_objects.call_interaction_page import CallInteractionPage
from step_definitions import agent_steps

CALL_INTERACTIONS = CallInteractionPage()


def handle_dnc_dialog(action='accept', timeout=10, force=False):
    for sec in range(timeout):
        if CALL_INTERACTIONS.get_dnc_dialog().is_displayed():
            if action == 'accept':
                CALL_INTERACTIONS.get_ok_dialog_button().click()
            else:
                CALL_INTERACTIONS.get_cancel_dialog_button().click()
            common.system_wait(1)
            if not CALL_INTERACTIONS.get_dnc_dialog().is_displayed():
                break
        if sec > 4 and not force:
            break


def check_script_call_tab():
    pass


@when(parsers.parse("I select {campaign} outbound campaign"))
def select_outbound_campaign(campaign):
    CALL_INTERACTIONS.get_outbound_campaigns_button().click()
    common.wait_element_attribute_contains(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.outbound_campaigns_button, 'aria-expanded', 'true')
    available_campaigns = CALL_INTERACTIONS.get_outbound_campaigns_options()
    for campaign_ in available_campaigns:
        if campaign_.text.strip() == campaign:
            campaign_.click()
            break
    common.wait_element_attribute_contains(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.outbound_campaigns_button, 'aria-expanded', 'false')


@when(parsers.parse("I call {number}"))
def call_number(number):
    agent_steps.AGENT_HOME.get_agent_voice_button().click()
    CALL_INTERACTIONS.get_number_input().clear()
    CALL_INTERACTIONS.get_number_input().send_keys(number)
    CALL_INTERACTIONS.get_dial_button().click()
    handle_dnc_dialog()
    common.wait_element_to_be_clickable(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.call_notification_dialog)
    CALL_INTERACTIONS.get_call_notification_dialog_ok_button().click()
    common.wait_elements_to_be_less_than(CALL_INTERACTIONS.driver, CALL_INTERACTIONS.call_notification_dialog, 1)


@when("I get the answer for the call")
def get_call_answer():
    pass


@when(parsers.parse("I check the call {tab} tab"))
def check_call_tab(tab):
    globals()['check_' + tab + '_call_tab']()
