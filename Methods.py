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
        method_mapper = {
            'IP-Whitelist': self.whitelist_ip()
        }
        method_response = method_mapper.get(self.issue_type)
        return method_response
