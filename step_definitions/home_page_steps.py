from page_objects.home_page import HomePage
from pytest_bdd import (
    when
)

HOME_PAGE = None


def set_pages(driver):
    # set all pages that will be used in the test
    global HOME_PAGE
    HOME_PAGE = HomePage(driver)


@when("I select adp from menu")
def select_adp(driver):
    set_pages(driver)
    HOME_PAGE.get_agent_span().click()
    HOME_PAGE.get_web_agent_item().click()
