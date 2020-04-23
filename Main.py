import Fields, conf, Outbound_Webhook, Methods
from flask import Flask, request

app = Flask(__name__)


def post_validation_success_comment(json_payload):
    outbound_webhook = Outbound_Webhook.NewOutboundWebhook(json_payload)
    outbound_webhook.create_approval_comment()


def post_validation_failure_comment(json_payload):
    outbound_webhook = Outbound_Webhook.NewOutboundWebhook(json_payload)
    outbound_webhook.create_denial_comment()


@app.route("/validate", methods=['POST'])
def validate_fields():
    json_payload = request.get_json()
    field_validator = Fields.Fields(json_payload)
    validation_results = field_validator.validate_customfields()
    for result in validation_results:
        if conf.validation_failure in result:
            post_validation_failure_comment(json_payload)
            return result
        else:
            post_validation_success_comment(json_payload)
    return 'Validation'


@app.route("/trigger_method", methods=['POST'])
def route_method():
    json_payload = request.get_json()
    method_router = Methods.Method(json_payload)
    method_router.route_method()
    return 'Method Routed'

app.run()