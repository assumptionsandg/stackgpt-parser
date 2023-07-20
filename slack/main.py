import os
import requests
import hmac
import hashlib
from celery import Celery, Task
from flask import Flask, Response, request, json

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

dt_run_url = "https://dust.tt/api/v1/w/b74db6909a/apps/ed5b092a75/runs"
dt_token = { "Content-type":"application/json", "Authorization": os.environ.get("DT_TOKEN") }
sl_headr = { "Content-type":"application/json", "Authorization": os.environ.get("SL_OAUTH") }
sl_token = os.environ.get("SL_TOKEN") #update to sign/secret
sl_secret = os.environ.get("SL_SIGN")

def auth(payload, sl_sign, sl_time):
    verf_string = ""
    for i in payload:
        verf_string += "{}={}".format(i, payload[i][0])
        if i != list(payload)[-1]:
            verf_string += "&"
    auth_string = "v0:{}:{}".format(sl_time, verf_string)
    print(auth_string)
    kb = bytes(sl_secret, 'ascii')
    db = bytes(auth_string, 'ascii')
    hash_string = hmac.new(kb, db, hashlib.sha256).hexdigest()
    print(hash_string)
    return "v0="+hash_string

@celery.task
def post_ai(payload):
    print(type(payload['message']))
    dt_run_obj = {
        "specification_hash": "e7911c156bff999f51498fe2d4ea027bb1fa7e41a07a1e6a637f184db704b0ec",
        "config": {"MODEL":{"provider_id":"openai","model_id":"gpt-3.5-turbo","function_call":None,"use_cache":True},"DATASOURCE":{"data_sources":[{"workspace_id":"b74db6909a","data_source_id":"kayobe"}],"top_k":12,"filter":{"tags":None,"timestamp":None},"use_cache":False}},
        "blocking": True,
        "inputs": [{ "question": payload['message']['text'] }]
    }
    dt_run_data = json.dumps(dt_run_obj)
    dt_run_request = requests.post(dt_run_url, headers=dt_token, data=dt_run_data)
    dt_run_json = json.loads(dt_run_request.text)
    #print(dt_run_json)
    dt_run_results = dt_run_json['run']['results'][0][0]['value']
    #print(payload['response_url'][0])
    dt_hook_post = requests.post("https://slack.com/api/chat.postMessage", headers=sl_headr, data=json.dumps({ "channel": payload['channel']['id'], "text":dt_run_results, "thread_ts":payload['message']['ts'] }))
    print(payload['channel']['id'], payload['message']['ts']) 

@app.route('/', methods=['POST'])
def ask():
    sl_sign = request.headers.get("X-Slack-Signature")
    sl_time = request.headers.get("X-Slack-Request-Timestamp")
    payload = request.form.to_dict(flat=False)
    json_payload = json.loads(payload['payload'][0])
   # if auth(payload, sl_sign, sl_time) == sl_sign): update to sign/secret
    if json_payload['token'] == sl_token: #insecure override
        print("authed")
        post_ai.delay(json_payload)
        response = app.response_class(
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            status=403,
            mimetype='application/json')
    return response
 


