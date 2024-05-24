from step_definitions import common_steps, adt_login_steps
from test.initialization import base_setup


def login_adt():
    base_setup.set_base_pages()
    common_steps.STARTED_PAGES.append(adt_login_steps.ADT_LOGIN_PAGE)
