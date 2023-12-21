from pytest_bdd import scenario


@scenario('../features/chat_simple_interaction.feature', "Check agent text interaction")
def test_check_simple_chat():
    pass
