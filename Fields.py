import conf
import ipaddress


class Fields:
    def __init__(self, json_payload):
        self.json_payload = json_payload
        self.validation_results = []
        self.issue_type = str(self.json_payload['fields']['issuetype']['name'])
        self.ip_address = str(self.json_payload['fields']['customfield_10065'])

    def validate_ip_network(self):
        ip_data = self.ip_address.replace(" ", "").replace("\r", "").split('\n')
        for ip in ip_data:
            try:
                ip_network_check = ipaddress.ip_network(ip)
            except Exception as e:
                print(e)
                return conf.validation_failure
        return conf.validation_success

    def validate_ip_global(self):
        ip_data = self.ip_address.replace(" ", "").replace("\r", "").split('\n')
        for ip in ip_data:
            ip_network_check = ipaddress.ip_network(ip)
            ip_is_global = ip_network_check.is_global
            if ip_is_global:
                valid = ip + ' is public'
            else:
                return conf.validation_failure
        return conf.validation_success

    # Master validation functions. The following functions should be all-inclusive of the functions required to validate
    # custom fields, per ticket type. Need to return false, or true based on the child validation functions (included in
    # the list
    def validate_ip_grammar(self):
        validation_result_list = [self.validate_ip_network(), self.validate_ip_global()]
        if conf.validation_failure in validation_result_list:
            return conf.validation_failure
        else:
            return conf.validation_success

    # Function to map a ticket type, to a master validation function, and append the result to the validation_results
    # list. Pass validation_results back to the main class for success/failure action
    def validate_customfields(self):
        customfield_validation_mapper = {
            'IP-Whitelist': self.validate_ip_grammar()
        }
        self.validation_results.append(customfield_validation_mapper.get(self.issue_type))
        print(self.validation_results)
        return self.validation_results
