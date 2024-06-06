from pytest_bdd import scenario


@scenario('../features/adapters/adt_plus_scenarios.feature', 'Check ADT basic calls')
def test_check_adt_basic_calls():
    pass
