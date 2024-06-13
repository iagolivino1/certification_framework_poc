from pytest_bdd import scenario


@scenario('../features/adp_text_interaction.feature', "Agent text interaction")
def test_check_simple_chat():
    pass
