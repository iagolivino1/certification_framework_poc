import common
from pytest_bdd import when
from page_objects.chat_interaction_page import ChatInteractionPage
from step_definitions import agent_steps

CHAT_INTERACTION_PAGE = ChatInteractionPage()
CURRENT_NUMBER_OF_CHAT_INTERACTIONS = 0


@when("I check new chat interaction")
def check_new_chat_interaction():
    global CURRENT_NUMBER_OF_CHAT_INTERACTIONS
    timeout = 10
    for time_ in range(timeout):
        CHAT_INTERACTION_PAGE.get_refresh_chats_button().click()
        if len(CHAT_INTERACTION_PAGE.get_all_chat_interactions()) > CURRENT_NUMBER_OF_CHAT_INTERACTIONS:
            print("CHAT INTERACTION FOUND!")
            CURRENT_NUMBER_OF_CHAT_INTERACTIONS = len(CHAT_INTERACTION_PAGE.get_all_chat_interactions())
            return
        common.system_wait(1)
    raise Exception(f"COULD NOT FIND CHAT INTERACTION DURING {timeout} SECONDS.")


@when("I select newest chat interaction")
def select_newest_chat_interaction(start_message):
    CHAT_INTERACTION_PAGE.get_unselected_lock_chat_button().click()
    CHAT_INTERACTION_PAGE.get_newest_chat_interaction().click()
    common.wait_page_element_load(CHAT_INTERACTION_PAGE.driver, CHAT_INTERACTION_PAGE.conversation_content)
    common.wait_element_attribute_contains(CHAT_INTERACTION_PAGE.driver, CHAT_INTERACTION_PAGE.conversation_content, 'innerText', start_message)


@when("I reply the chat message")
def reply_chat(reply_message):
    common.system_wait(2)
    common.switch_tabs(CHAT_INTERACTION_PAGE.driver, tab_title='Agent Desktop Plus')
    CHAT_INTERACTION_PAGE.get_reply_message_textarea().send_keys(reply_message)
    CHAT_INTERACTION_PAGE.get_send_message_button().click()


@when("I dispose the chat interaction")
def dispose_chat():
    common.switch_tabs(CHAT_INTERACTION_PAGE.driver, tab_title='Agent Desktop Plus')
    common.wait_element_to_be_clickable(CHAT_INTERACTION_PAGE.driver, CHAT_INTERACTION_PAGE.set_disposition_button)
    CHAT_INTERACTION_PAGE.get_set_disposition_button().click()
    common.wait_page_element_load(CHAT_INTERACTION_PAGE.driver, agent_steps.AGENT_HOME.no_disposition_option)
    agent_steps.AGENT_HOME.get_no_disposition_option().click()
    common.wait_elements_to_be_less_than(CHAT_INTERACTION_PAGE.driver, CHAT_INTERACTION_PAGE.newest_chat_interaction, 1)
