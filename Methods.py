import Outbound_Webhook


class Method:
    def __init__(self, json_payload):
        self.json_payload = json_payload
        self.issue_type = str(self.json_payload['fields']['issuetype']['name'])

    def parse_data_for_avx(self):
        return 'Data Parsed for AVX call'

    def make_avx_whitelisting_call(self):
        return 'response to scheduled avx task'


    def whitelist_ip(self):
        method_functions = []
        return method_functions

    def route_method(self):
        Outbound_Webhook.send_splunk_notice(f"Automation method triggered for ticket number: {self.json_payload['key']} with an issue type of: {self.issue_type}")
        method_mapper = {
            'IP-Whitelist': self.whitelist_ip()
        }
        method_response = method_mapper.get(self.issue_type)
        return method_response
