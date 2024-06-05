from selenium.webdriver.common.by import By


class ADTAdapterPage(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.url = ''
        self.content_header = "//h1"
        self.station_setup = "//div[@data-f9-template='station-setup-container']"
        self.softphone_station_option = "//input[@id='station_SOFTPHONE']"
        self.webrtc_station_option = "//input[@id='station_WEBRTC']"
        self.pstn_station_option = "//input[@id='station_PSTN']"
        self.gateway_station_option = "//input[@id='station_GATEWAY']"
        self.none_station_option = "//input[@id='station_EMPTY']"
        self.station_number_input = "//input[@id='station_number']"
        self.remember_my_selection_checkbox = "//input[@id='remember_station']"
        self.confirm_selection_button = "//button[contains(text(), 'Confirm')]"
        self.station_setup_devices = "//div[@data-f9-template='setup-devices']"
        self.reset_station_button = "//button[@id='restart-softphone']"
        self.station_connection_status = "//div[@class='softphone-status-bar']//span[not(contains(@class, 'stationType'))]"
        self.loading_label = "//i[@class='fa fa-spinner fa-spin']/.."
        self.agent_home_panel = "//div[@id='home-panel']"
        self.agent_state_button = "//button[@id='agent-readyState']"
        self.ready_for_last_selection_option = "//li[@id='ready_state_all']/a"
        self.ready_for_options = "//li[@id='ready_state_ready_for']/a"
        self.not_ready_option = "//li[@id='not_ready_-1']/a"
        self.logout_button = "//span[@id='logout']/a"
        self.voice_channel_checkbox = "//input[@id='channel_CALL']"
        self.voicemail_channel_checkbox = "//input[@id='channel_VOICE_MAIL']"
        self.make_a_call_button = "//button[@id='newCall-btn']"
        self.voicemail_button = "//span[@id='voicemails_counter']/.."
        self.reminders_button = "//span[@id='callbacks_counter']/.."
        self.messages_button = "//button[@id='showInternalMessages-btn']"
        self.missed_calls_button = "//button[@id='missed-calls-btn']"
        self.address_book_button = "//button[@id='home-panel-address-book-btn']"
        self.queue_stats_button = "//button[@id='queueStats-btn']"
        self.add_to_dnc_button = "//button[@id='dnc-btn']"
        self.settings_button = "//button[@id='settings-btn']"
        self.help_button = "//button[@id='help-menu-btn']"
        self.new_call_panel = "//header[contains(text(), 'New Call')]/.."
        self.contact_call_input = "//input[@id='select_contact_call_number']"
        self.select_campaign_button = "//button[@id='newCallCampaign_btn']"
        self.campaign_options = "//div[@id='campaign_dropdownlist']//li"
        self.dial_button = "//button[@id='dial_btn']"
        self.new_call_panel_text = "//div[@class='dialog_text_wrapper']"
        self.do_not_call_dial_button = "//button[@id='btn_dial']"
        self.do_not_call_cancel_button = "//button[@id='dtn_cancel']"
        self.agent_call_panel = "//header[contains(text(), 'Agent Call')]/.."
        self.all_tools_toggle = "//div[@id='all-tools-toggle']"
        self.script_button = "//button[@id='script_btn']"
        self.worksheet_button = "//button[@id='worksheet_btn']"
        self.set_disposition_button = "//button[@id='call_endInteractionBtn']"
        self.dispositions_view = "//div[@class='dispositions-view']"
        self.dispositions_list = "//div[@id='dispFilteredList_call']//li"
        self.selected_disposition = "//label[contains(., '<text>')]/../input"
        self.end_call_interaction_button = "//button[@id='setDisposition_call']"
        self.inbound_call_panel = "//header[contains(text(), 'Inbound Call')]/.."
        self.active_call_type = "//p[@id='active_callType']"
        self.active_caller_name = "//p[@id='active_callerName']"

    def get_content_header(self):
        return self.driver.find_element(By.XPATH, self.content_header)

    def get_station_setup(self):
        return self.driver.find_element(By.XPATH, self.station_setup)

    def get_softphone_station_option(self):
        return self.driver.find_element(By.XPATH, self.softphone_station_option)

    def get_webrtc_station_option(self):
        return self.driver.find_element(By.XPATH, self.webrtc_station_option)

    def get_pstn_station_option(self):
        return self.driver.find_element(By.XPATH, self.pstn_station_option)

    def get_gateway_station_option(self):
        return self.driver.find_element(By.XPATH, self.gateway_station_option)

    def get_none_station_option(self):
        return self.driver.find_element(By.XPATH, self.none_station_option)

    def get_station_number_input(self):
        return self.driver.find_element(By.XPATH, self.station_number_input)

    def get_remember_my_selection_checkbox(self):
        return self.driver.find_element(By.XPATH, self.remember_my_selection_checkbox)

    def get_confirm_selection_button(self):
        return self.driver.find_element(By.XPATH, self.confirm_selection_button)

    def get_station_setup_devices(self):
        return self.driver.find_elements(By.XPATH, self.station_setup_devices)

    def get_reset_station_button(self):
        return self.driver.find_element(By.XPATH, self.reset_station_button)

    def get_station_connection_status(self):
        return self.driver.find_element(By.XPATH, self.station_connection_status)

    def get_loading_label(self):
        return self.driver.find_element(By.XPATH, self.loading_label)

    def get_agent_home_panel(self):
        return self.driver.find_element(By.XPATH, self.agent_home_panel)

    def get_agent_state_button(self):
        return self.driver.find_element(By.XPATH, self.agent_state_button)

    def get_ready_for_last_selection_option(self):
        return self.driver.find_element(By.XPATH, self.ready_for_last_selection_option)

    def get_ready_for_options(self):
        return self.driver.find_element(By.XPATH, self.ready_for_options)

    def get_not_ready_option(self):
        return self.driver.find_element(By.XPATH, self.not_ready_option)

    def get_logout_button(self):
        return self.driver.find_element(By.XPATH, self.logout_button)

    def get_voice_channel_checkbox(self):
        return self.driver.find_element(By.XPATH, self.voice_channel_checkbox)

    def get_voicemail_channel_checkbox(self):
        return self.driver.find_element(By.XPATH, self.voicemail_channel_checkbox)

    def get_make_a_call_button(self):
        return self.driver.find_element(By.XPATH, self.make_a_call_button)

    def get_voicemail_button(self):
        return self.driver.find_element(By.XPATH, self.voicemail_button)

    def get_reminders_button(self):
        return self.driver.find_element(By.XPATH, self.reminders_button)

    def get_messages_button(self):
        return self.driver.find_element(By.XPATH, self.messages_button)

    def get_missed_calls_button(self):
        return self.driver.find_element(By.XPATH, self.missed_calls_button)

    def get_address_book_button(self):
        return self.driver.find_element(By.XPATH, self.address_book_button)

    def get_queue_stats_button(self):
        return self.driver.find_element(By.XPATH, self.queue_stats_button)

    def get_add_to_dnc_button(self):
        return self.driver.find_element(By.XPATH, self.add_to_dnc_button)

    def get_settings_button(self):
        return self.driver.find_element(By.XPATH, self.settings_button)

    def get_help_button(self):
        return self.driver.find_element(By.XPATH, self.help_button)

    def get_new_call_panel(self):
        return self.driver.find_element(By.XPATH, self.new_call_panel)

    def get_contact_call_input(self):
        return self.driver.find_element(By.XPATH, self.contact_call_input)

    def get_select_campaign_button(self):
        return self.driver.find_element(By.XPATH, self.select_campaign_button)

    def get_campaign_options(self):
        return self.driver.find_elements(By.XPATH, self.campaign_options)

    def get_dial_button(self):
        return self.driver.find_element(By.XPATH, self.dial_button)

    def get_new_call_panel_text(self):
        return self.driver.find_element(By.XPATH, self.new_call_panel_text)

    def get_do_not_call_dial_button(self):
        return self.driver.find_element(By.XPATH, self.do_not_call_dial_button)

    def get_do_not_call_cancel_button(self):
        return self.driver.find_element(By.XPATH, self.do_not_call_cancel_button)

    def get_agent_call_panel(self):
        return self.driver.find_element(By.XPATH, self.agent_call_panel)

    def get_all_tools_toggle(self):
        return self.driver.find_element(By.XPATH, self.all_tools_toggle)

    def get_script_button(self):
        return self.driver.find_element(By.XPATH, self.script_button)

    def get_worksheet_button(self):
        return self.driver.find_element(By.XPATH, self.worksheet_button)

    def get_set_disposition_button(self):
        return self.driver.find_element(By.XPATH, self.set_disposition_button)

    def get_dispositions_view(self):
        return self.driver.find_element(By.XPATH, self.dispositions_view)

    def get_dispositions_list(self):
        return self.driver.find_elements(By.XPATH, self.dispositions_list)

    def get_selected_disposition(self, text=''):
        return self.driver.find_element(By.XPATH, self.selected_disposition.replace('<text>', text))

    def get_end_call_interaction_button(self):
        return self.driver.find_element(By.XPATH, self.end_call_interaction_button)

    def get_inbound_call_panel(self):
        return self.driver.find_element(By.XPATH, self.inbound_call_panel)

    def get_active_call_type(self):
        return self.driver.find_element(By.XPATH, self.active_call_type)

    def get_active_caller_name(self):
        return self.driver.find_element(By.XPATH, self.active_caller_name)
