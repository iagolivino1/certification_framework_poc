from pytest_bdd import scenario


@scenario('../features/adapters/netsuite_scenarios.feature', 'Check NetSuite basic calls')
def test_check_netsuite_basic_calls():
    pass
