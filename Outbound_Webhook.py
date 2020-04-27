import requests, json, secure_conf, conf
from requests.auth import HTTPBasicAuth


class NewOutboundWebhook:
    def __init__(self, json_payload):
        self.original_json_payload = json_payload
        self.create_comment_url = conf.jiraFQDN + "/rest/servicedeskapi/request/" + \
                                  self.original_json_payload['key'] + "/comment"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

    def create_approval_comment(self):
        comment_payload = json.dumps({
            "public": True,
            "body": "Automation field validation completed. Awaiting manager approval"
        })
        requests.request("POST", self.create_comment_url, data=comment_payload, headers=self.headers,
                         auth=HTTPBasicAuth(secure_conf.username, secure_conf.api_token))

    def create_denial_comment(self):
        comment_payload = json.dumps({
            "public": True,
            "body": "Automation field validation failed. Please try again."
        })
        requests.request("POST", self.create_comment_url, data=comment_payload, headers=self.headers,
                         auth=HTTPBasicAuth(secure_conf.username, secure_conf.api_token))

    def create_errmsg_comment(self, errmsg):
        comment_payload = json.dumps({
            "public": True,
            "body": str(errmsg)
        })
        requests.request("POST", self.create_comment_url, data=comment_payload, headers=self.headers,
                         auth=HTTPBasicAuth(secure_conf.username, secure_conf.api_token))
