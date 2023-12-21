import common
from pytest_bdd import (
    given,
    when
)


@when("I check the second browser tab opened")
def check_new_tab(driver):
    common.switch_tabs(driver)
