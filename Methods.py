from ipaddress import IPv4Interface
import Outbound_Webhook, conf


class Method:
    def __init__(self, json_payload):
        self.json_payload = json_payload
        self.jira_comment = Outbound_Webhook.NewOutboundWebhook(self.json_payload)
        self.issue_type = str(self.json_payload['fields']['issuetype']['name'])
        self.ticket_id = str(self.json_payload['key'])

    def parse_avx_wl_data(self):
        ip_address = str(self.json_payload['fields']['customfield_10065'])
        client_url = str(self.json_payload['fields']['customfield_10066'])
        client_name = str(self.json_payload['fields']['customfield_10063'])
        ip_data = ip_address.replace(" ", "/").replace("\r", "").replace("//", "/").split('\n')
        client_name = "ACE"
        for ip in ip_data:
            interface = IPv4Interface(ip)
            update = interface.with_netmask.replace("/255.255.255.255", "").replace("/", " ")
        avx_payload = {
            "payload": {
                "data": {
                    "input": {
                        "requestData": [
                            {
                                "sequenceNo": 1,
                                "scenario": "scenario",
                                "fieldInfo": {
                                    "start_time": "<mandatory field>",
                                    "client_url": client_url,
                                    "ticket_number": self.ticket_id,
                                    "client_name": client_name,
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
        return avx_payload

    def make_avx_wl_call(self, data):
        return 'Whitelisting call made', data

    def whitelist_ip(self):
        avx_parsed_wl_data = self.parse_avx_wl_data()
        self.make_avx_wl_call(avx_parsed_wl_data)
        return f'Whitelisting Event made for {self.ticket_id}.'

    def route_method(self):
        Outbound_Webhook.send_splunk_notice(
            f"Automation method triggered for ticket number: {self.json_payload['key']} with an issue type of: {self.issue_type}")
        self.jira_comment.create_jira_comment(f"Automation method triggered. Method type: {self.issue_type}")
        method_mapper = {
            'IP-Whitelist': self.whitelist_ip()
        }
        method_response = method_mapper.get(self.issue_type)
        return method_response
