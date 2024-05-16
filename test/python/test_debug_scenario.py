from pytest_bdd import scenario


@scenario('../features/debug_scenario.feature', 'Debug scenario')
def test_debug_scenario():
    pass
