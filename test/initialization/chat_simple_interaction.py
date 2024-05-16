from common import get_config_file_section
from test.initialization import base_setup
from step_definitions import chat_template_steps, common_steps


def check_agent_text_interaction():
    lab_config = f"configuration/lab/{get_config_file_section('config.yml', 'configuration').get('lab')}.yml"
    base_setup.set_base_pages(2)
    common_steps.STARTED_PAGES.append(chat_template_steps.CHAT_TEMPLATE)
    chat_template_steps.CHAT_TEMPLATE.url = get_config_file_section(lab_config, 'configuration').get('chat_console_url')
