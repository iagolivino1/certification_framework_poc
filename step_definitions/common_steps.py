import common
from page_objects.common_page import CommonPage
from pytest_bdd import when

from step_definitions import login_steps

COMMON_PAGE = CommonPage()


def reset_variables():
    """
    reset all variables to avoid missmatch use when run more than 1 test at once
    """
    pass


def get_free_agent():
    agent = {}
    for agent_ in login_steps.AGENT_CREDENTIALS:
        is_free = login_steps.AGENT_CREDENTIALS.get(agent_).get('free')
        if is_free or is_free is None:
            agent = login_steps.AGENT_CREDENTIALS.get(agent_)
            agent['free'] = False
            login_steps.AGENT_CREDENTIALS[agent_] = agent
            break
    if not agent:
        raise Exception('no free agent available')
    return agent


@when("I check the second browser tab opened")
def check_new_tab():
    common.switch_tabs(COMMON_PAGE.driver)
