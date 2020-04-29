import ipaddress
from ipaddress import IPv4Interface

class Method:
    def __init__(self, json_payload):
        self.json_payload = json_payload
        self.issue_type = str(self.json_payload['fields']['issuetype']['name'])
        self.ip_address = str(self.json_payload['fields']['customfield_10065'])
        self.client_url = str(self.json_payload['fields']['customfield_10066'])
        self.client_name = str(self.json_payload['fields']['customfield_10063'])
        self.ticket_id = str(self.json_payload['key'])

    def make_avx_whitelisting_call(self):
        ip_data = self.ip_address.replace(" ", "/").replace("\r", "").replace("//", "/").split('\n')
        client_name = "ACE"
        for ip in ip_data:
            interface = IPv4Interface(ip)
            update = interface.with_netmask.replace("/255.255.255.255", "").replace("/", " ")
        avx_payload = {
            "payload": {
                "data": {
                    "input":{
                        "requestData": [
                            {
                                "sequenceNo": 1,
                                "scenario": "scenario",
                                "fieldInfo": {
                                    "start_time": "<mandatory field>",
                                    "client_url": self.client_url,
                                    "ticket_number": self.ticket_id,
                                    "client_name": self.client_name,
                                    "public_ip": update,
                                }
                            }
                        ]
                    },
                    "task_action": 1
                },
                "header": {
                    "workflowName": "ip_whitelist"
                }
            }
        }
        print(avx_payload)
        return "PASS"

    def whitelist_ip(self):
        method_functions = []
        return method_functions

    def route_method(self):
        method_mapper = {
            'IP-Whitelist': self.make_avx_whitelisting_call()
        }
        method_response = method_mapper.get(self.issue_type)
        return method_response
