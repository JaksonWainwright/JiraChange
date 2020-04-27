class Method:
    def __init__(self, json_payload):
        self.json_payload = json_payload
        self.issue_type = str(self.json_payload['fields']['issuetype']['name'])

    def whitelist_ip(self):
        self.security_scan()
        return 'True'


    def route_method(self):
        method_mapper = {
            'IP-Whitelist': self.whitelist_ip()
        }
        method_response = method_mapper.get(self.issue_type)
        return method_response
