import common
from page_objects.sf_agent_home_page import SFAgentHomePage
from pytest_bdd import when, parsers
from step_definitions import call_interaction_steps, common_steps

AGENT_HOME = SFAgentHomePage()


@when("I switch to Softphone Iframe")
def switch_to_iframe():
    common.switch_to_frame(AGENT_HOME.driver, AGENT_HOME.get_iframe_softphone())
    common.wait_page_element_load(AGENT_HOME.driver, AGENT_HOME.iframe_user_input)

@when("I see the SF agent logged in")
def see_agent_home_page():
    common.wait_element_to_be_clickable(AGENT_HOME.driver, AGENT_HOME.agent_state_button)