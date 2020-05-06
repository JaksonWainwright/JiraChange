import Fields, conf, Outbound_Webhook, Methods, secure_conf
from flask import Flask, request
from Outbound_Webhook import Jira_Transition


app = Flask(__name__)


@app.route("/validate", methods=['POST'])
def validate_fields():
    json_payload = request.get_json()
    field_validator = Fields.Fields(json_payload)
    validation_results = field_validator.validate_customfields()
    for result in validation_results:
        if conf.validation_failure in result:
            Outbound_Webhook.send_splunk_warning(f"Automation Field Validation failed. Ticket number: {json_payload['key']}")
            Outbound_Webhook.create_jira_denial_comment(json_payload)
            Outbound_Webhook.push_jira_transition(json_payload, Jira_Transition.validation_failed)
            return result
        else:
            Outbound_Webhook.send_splunk_notice(f"Automation Field Validation passed. Ticket number: {json_payload['key']}")
            Outbound_Webhook.create_jira_approval_comment(json_payload)
            Outbound_Webhook.push_jira_transition(json_payload, Jira_Transition.validation_succeeded)
    return 'Validation passed'


@app.route("/trigger_method", methods=['POST'])
def route_method():
    json_payload = request.get_json()
    method_router = Methods.Method(json_payload)
    method_response = method_router.route_method()
    return method_response


app.run()
