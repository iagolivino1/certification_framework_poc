import common
from page_objects.sf_agent_home_page import SFAgentHomePage
from pytest_bdd import when, parsers
from step_definitions import call_interaction_steps, common_steps

SF_AGENT_HOME = SFAgentHomePage()


@when("I see the agent SF home page")
def see_agent_home_page():
    common.wait_element_to_be_clickable(SF_AGENT_HOME.driver, SF_AGENT_HOME.agent_state_button)