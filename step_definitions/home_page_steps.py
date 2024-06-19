import common
from page_objects.home_page import HomePage
from pytest_bdd import when
from step_definitions import common_steps

HOME_PAGE = HomePage()


@when("I select adp from menu")
def select_adp():
    HOME_PAGE.get_agent_span().click()
    HOME_PAGE.get_web_agent_item().click()
    common.LOGGER.info(agent=common_steps.get_agent_for_logs(), message="adp option selected")
