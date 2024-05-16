from pytest_bdd import scenario


@scenario('../features/adp_scenarios.feature', 'Check basic calls')
def test_check_basic_calls():
    pass
