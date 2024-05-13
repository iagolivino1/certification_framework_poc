import driver
from step_definitions import call_interaction_steps, common_steps
from test.initialization import base_setup


def check_basic_calls():
    # base_setup.set_base_pages(2)
    base_setup.set_base_pages()
    common_steps.STARTED_PAGES.append(call_interaction_steps.CALL_INTERACTIONS)
