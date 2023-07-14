import os
import requests
import json

ol_token = { "Authorization": os.environ.get('OL_TOKEN') }
dt_token = { "Authorization": os.environ.get('DT_TOKEN') }

collections_api_url = "https://wiki.stackhpc.com/api/collections.list" 
documents_api_url = "https://wiki.stackhpc.com/api/documents.list"
datasource_doc_url = "https://dust.tt/api/v1/w/b74db6909a/data_sources/kayobe/documents/"

collections_api_obj = { "offset": 0 }

collections_api_req = requests.post(collections_api_url, headers=ol_token, data=collections_api_obj)
collections_api_req_obj = json.loads(collections_api_req.text)

documents_api_obj = { "limit": "50", "collectionId": collections_api_req_obj['data'][9]['id'] }
documents_api_req = requests.post(documents_api_url, headers=ol_token, data=documents_api_obj)
documents_api_req_obj = json.loads(documents_api_req.text)

for i in documents_api_req_obj['data']:
    for exluced_chars in ["/", "\\", "\n", "*", " ", "`", "#", "<", ">", ":", ".", "$", "\"", "\'", "-", ",", "(", ")", "?", "%", "[", "]", "_", ";", "&", "“", "”", "’", ]:
        if exluced_chars in i['text']:
            i['text']=i['text'].replace(exluced_chars,"")
    datasource_api_obj = { "text": i['text'] }
    print(datasource_api_obj)
    datasource_doc_req = requests.post(datasource_doc_url+i['title'].replace(" ", ""), headers=dt_token, data=datasource_api_obj)
    print(datasource_doc_req.text)

