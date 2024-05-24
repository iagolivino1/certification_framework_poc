from pytest_bdd import scenario


@scenario('../features/adt_plus_scenarios.feature', 'Login ADT')
def test_check_login_adt():
    pass
