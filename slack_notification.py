import requests
import json

def post_to_slack(text):
    slack_webhook_url = "user-slack-webhook-url"
    headers = { "Content-type": "application/json" }
    data = { "text" : text }
    res = requests.post(slack_webhook_url, headers=headers, data=json.dumps(data))