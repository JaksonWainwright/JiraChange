import conf, Outbound_Webhook
import ipaddress


class Fields:
    def __init__(self, json_payload):
        self.json_payload = json_payload
        self.validation_results = []
        self.jira_comment = Outbound_Webhook.NewOutboundWebhook(self.json_payload)
        self.issue_type = str(self.json_payload['fields']['issuetype']['name'])

<<<<<<< HEAD
    def parse_ip_customfield(self):
=======
    def parse_ip_customfields(self):
>>>>>>> 6a9ec20031b12b73c457c58b9041e9c1c9174fbc
        ip_addresses = str(self.json_payload['fields']['customfield_10065'])
        ip_data = ip_addresses.replace(" ", "/").replace("\r", "").replace("//", "/").split('\n')
        return ip_data

    def validate_ip_network(self):
<<<<<<< HEAD
        for ip_address in self.parse_ip_customfield():
=======
        for ip_address in self.parse_ip_customfields():
>>>>>>> 6a9ec20031b12b73c457c58b9041e9c1c9174fbc
            try:
                ip_network_check = ipaddress.ip_network(ip_address)
            except Exception as errmsg:
                self.jira_comment.create_jira_comment(errmsg)
                return conf.validation_failure
        return conf.validation_success

    def validate_ip_global(self):
<<<<<<< HEAD
        for ip_address in self.parse_ip_customfield():
=======
        for ip_address in self.parse_ip_customfields():
>>>>>>> 6a9ec20031b12b73c457c58b9041e9c1c9174fbc
            try:
                ip_network_check = ipaddress.ip_network(ip_address)
                ip_is_global = ip_network_check.is_global
                if not ip_is_global:
                    self.jira_comment.create_jira_comment(f'{ip_address} is a private IP address')
                    return conf.validation_failure
            except Exception as errmsg:
                print(errmsg)
                return conf.validation_failure
        return conf.validation_success

    def validate_wl_url(self):
        valid_urls = ['ganal']

    def validate_ip_grammar(self):
        validation_results = [self.validate_ip_network(), self.validate_ip_global()]
        if conf.validation_failure in validation_results[0]:
            return conf.validation_failure
        elif conf.validation_failure in validation_results[1:]:
            return conf.validation_failure
        else:
            return conf.validation_success

    def validate_customfields(self):
        Outbound_Webhook.send_splunk_notice(f"Field validation started on ticket number: {self.json_payload['key']}")
        customfield_validation_mapper = {
            'IP-Whitelist': self.validate_ip_grammar()
        }
        self.validation_results.append(customfield_validation_mapper.get(self.issue_type))
        print(self.validation_results)
        return self.validation_results
