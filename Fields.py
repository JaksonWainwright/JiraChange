import conf


class Fields:
    def __init__(self, json_payload):
        self.json_payload = json_payload
        self.validation_results = []
        self.issue_type = str(self.json_payload['fields']['issuetype']['name'])

    def validate_ip_grammar(self):
        e = 'Error reason'
        return conf.validation_failure

    def validate_customfields(self):
        customfield_validation_mapper = {
            'IP-Whitelist': self.validate_ip_grammar()
        }
        self.validation_results.append(customfield_validation_mapper.get(self.issue_type))
        print(self.validation_results)
        return self.validation_results
