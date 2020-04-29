import Fields, conf, Outbound_Webhook, Methods
from flask import Flask, request

app = Flask(__name__)


# Functions for adding success or failure validation messages
def post_validation_success_comment(json_payload):
    outbound_webhook = Outbound_Webhook.NewOutboundWebhook(json_payload)
    outbound_webhook.create_jira_approval_comment()


def post_validation_failure_comment(json_payload):
    outbound_webhook = Outbound_Webhook.NewOutboundWebhook(json_payload)
    outbound_webhook.create_jira_denial_comment()


# Validate route, to trigger field validation, field validation is based on ticket type
@app.route("/validate", methods=['POST'])
def validate_fields():
    json_payload = request.get_json()
    field_validator = Fields.Fields(json_payload)
    validation_results = field_validator.validate_customfields()
    for result in validation_results:
        if conf.validation_failure in result:
            Outbound_Webhook.send_splunk_warning(f"Automation Field Validation failed. Ticket number: {json_payload['key']}")
            post_validation_failure_comment(json_payload)
            return result
        else:
            Outbound_Webhook.send_splunk_notice(f"Automation Field Validation passed. Ticket number: {json_payload['key']}")
            post_validation_success_comment(json_payload)
    return 'Validation passed'


# Trigger method method, to trigger the method, based on ticket type
@app.route("/trigger_method", methods=['POST'])
def route_method():
    json_payload = request.get_json()
    method_router = Methods.Method(json_payload)
    method_router.route_method()
    return 'Method Routed'


app.run()
