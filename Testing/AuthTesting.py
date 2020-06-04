from flask import Flask, request

app = Flask(__name__)

@app.route("/authenticate_webhook", methods=['POST', 'GET'])
def jira_webhook_auth():
    params = request.args.get('token')
    print(params)
    return "see output"


if __name__ == '__main__':
    app.run()