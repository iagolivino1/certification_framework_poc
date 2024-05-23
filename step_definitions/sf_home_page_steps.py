import common
from page_objects.sf_home_page import SFHomePage
from pytest_bdd import when


HOME_PAGE = SFHomePage()


@when("I switch to Softphone Iframe")
def switch_to_iframe():
    common.switch_to_frame(HOME_PAGE.driver, HOME_PAGE.get_iframe_softphone())
    common.wait_page_element_load(HOME_PAGE.driver, HOME_PAGE.iframe_user_input)