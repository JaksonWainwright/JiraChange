class Method:
    def __init__(self, json_payload):
        self.json_payload = json_payload
        self.issue_type = str(self.json_payload['fields']['issuetype']['name'])

    def whitelist_ip(self):
        return 'True'

    def route_method(self):
        method_mapper = {
            'IP-Whitelist': self.whitelist_ip()
        }

        return 'Method Routed'