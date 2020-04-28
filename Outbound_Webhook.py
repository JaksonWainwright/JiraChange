import requests, json, secure_conf, conf
from requests.auth import HTTPBasicAuth


# File to handle all outbound webhooks, mostly back to Jira. Possible for other places, such as Mattermost.
# Purely for informational webhooks. Any webhooks to trigger automation need to have it
class NewOutboundWebhook:
    def __init__(self, json_payload):
        self.original_json_payload = json_payload
        self.jira_comment_endpoint = conf.jiraFQDN + "/rest/servicedeskapi/request/" + self.original_json_payload['key'] + "/comment"
        self.jira_reqd_headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

    def create_jira_approval_comment(self):
        comment_payload = json.dumps({
            "public": True,
            "body": "Automation field validation completed. Awaiting manager approval"
        })
        requests.request("POST", self.jira_comment_endpoint, data=comment_payload, headers=self.jira_reqd_headers,
                         auth=HTTPBasicAuth(secure_conf.jira_username, secure_conf.jira_api_token))

    def create_jira_denial_comment(self):
        comment_payload = json.dumps({
            "public": True,
            "body": "Automation field validation failed. Please try again."
        })
        requests.request("POST", self.jira_comment_endpoint, data=comment_payload, headers=self.jira_reqd_headers,
                         auth=HTTPBasicAuth(secure_conf.jira_username, secure_conf.jira_api_token))

    def create_jira_errmsg_comment(self, errmsg):
        comment_payload = json.dumps({
            "public": True,
            "body": str(errmsg)
        })
        requests.request("POST", self.jira_comment_endpoint, data=comment_payload, headers=self.jira_reqd_headers,
                         auth=HTTPBasicAuth(secure_conf.jira_username, secure_conf.jira_api_token))
