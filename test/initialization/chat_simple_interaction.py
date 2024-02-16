import driver
from test.initialization import base_setup
from step_definitions import chat_template_steps


def check_agent_text_interaction():
    base_setup.set_base_pages(2)
    chat_template_steps.CHAT_TEMPLATE.driver = driver.DRIVERS[1]
