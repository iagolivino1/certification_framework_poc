import common
from page_objects.common_page import CommonPage
from pytest_bdd import (
    given,
    when
)

COMMON_PAGE = CommonPage()


def reset_variables():
    """
    reset all variables to avoid missmatch use when run more than 1 test at once
    """
    pass


@when("I check the second browser tab opened")
def check_new_tab():
    common.switch_tabs(COMMON_PAGE.driver)
