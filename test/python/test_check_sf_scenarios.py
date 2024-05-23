from pytest_bdd import scenario


@scenario('../features/sf_scenarios.feature', 'Check sf basic calls')
def test_check_sf_basic_calls():
    pass