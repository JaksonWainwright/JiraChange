import requests, json, secure_conf, conf, Syslog_Client
from requests.auth import HTTPBasicAuth


def send_splunk_notice(errmsg):
    log = Syslog_Client.Syslog('35.194.20.71')
    log.send(errmsg, Syslog_Client.Level.NOTICE)


def send_splunk_warning(errmsg):
    log = Syslog_Client.Syslog('35.194.20.71')
    log.send(errmsg, Syslog_Client.Level.NOTICE)


class NewOutboundWebhook:
    def __init__(self, json_payload):
        self.original_json_payload = json_payload
        self.jira_comment_endpoint = conf.jiraFQDN + "/rest/servicedeskapi/request/" + self.original_json_payload['key'] + "/comment"
        self.jira_reqd_headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

    def jira_request(self, request_body):
        requests.request("POST", self.jira_comment_endpoint, data=request_body, headers=self.jira_reqd_headers,
                         auth=HTTPBasicAuth(secure_conf.jira_username, secure_conf.jira_api_token))

    def create_jira_approval_comment(self):
        comment_payload = json.dumps({
            "public": True,
            "body": "Automation field validation completed. Awaiting manager approval"
        })
        self.jira_request(comment_payload)

    def create_jira_denial_comment(self):
        comment_payload = json.dumps({
            "public": True,
            "body": "Automation field validation failed. Please try again."
        })
        self.jira_request(comment_payload)

    def create_jira_comment(self, comment):
        comment_payload = json.dumps({
            "public": True,
            "body": str(comment)
        })
        self.jira_request(comment_payload)



