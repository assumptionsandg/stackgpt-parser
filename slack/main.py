import os
import requests
from flask import Flask, Response, request, json
from slack_sdk import WebClient

app = Flask(__name__)

"""
slack_secret = os.environ('SLACK_SIGNING_SECRET')
slack_token = os.environ('SLACK_BOT_TOKEN')
slack_client = WebClient(slack_token)
"""

dt_run_url = "https://dust.tt/api/v1/w/b74db6909a/apps/ed5b092a75/runs"
dt_token = { "Content-type":"application/json", "Authorization": os.environ.get("DT_TOKEN") }

@app.route('/', methods=['POST'])
def ask():
    payload = request.form.to_dict(flat=False)
    print(payload['text'][0])
    dt_run_obj = {
      "specification_hash": "e7911c156bff999f51498fe2d4ea027bb1fa7e41a07a1e6a637f184db704b0ec",
      "config": {"MODEL":{"provider_id":"openai","model_id":"gpt-3.5-turbo","function_call":None,"use_cache":True},"DATASOURCE":{"data_sources":[{"workspace_id":"b74db6909a","data_source_id":"kayobe"}],"top_k":12,"filter":{"tags":None,"timestamp":None},"use_cache":False}},
      "blocking": True,
      "inputs": [{ "question": payload['text'][0] }]
    }
    dt_run_data = json.dumps(dt_run_obj)
    dt_run_request = requests.post(dt_run_url, headers=dt_token, data=dt_run_data)
    dt_run_json = json.loads(dt_run_request.text)
    dt_run_results = dt_run_json['run']['results'][0][0]['value']
    dt_return_obj = { "blocks": [{ "type": "section", "text": { "type": "mrkdwn", "text": dt_run_results } }] }
    response = app.response_class(
        response=json.dumps(dt_return_obj),
        status=200,
        mimetype='application/json'
    )
    return response 

    