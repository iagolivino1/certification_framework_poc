from common import get_config_file_section
from step_definitions import call_interaction_steps, common_steps
from test.initialization import base_setup


def check_basic_calls():
    base_setup.set_base_pages(2)
    common_steps.STARTED_PAGES.append(call_interaction_steps.CALL_INTERACTIONS)

    # set connector url if any
    lab_config = f"configuration/lab/{get_config_file_section('config.yml', 'configuration').get('lab')}.yml"
    connector_url_ = get_config_file_section(lab_config, 'configuration').get('connector_url')
    if connector_url_:
        call_interaction_steps.CALL_INTERACTIONS.connector_url = connector_url_
