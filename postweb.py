# resuests モジュールをインポート
from urllib import response
from urllib.request import urlopen
from matplotlib.font_manager import json_dump
import requests
import json
import logging
import http.client
import os.path
logging.basicConfig(level=logging.DEBUG)
http.client.HTTPConnection.debuglevel = 1

def upload_redmine(filepath):
    myheaders = {
            'Content-Type': 'application/octet-stream',
            'X-Redmine-API-Key': '2b002da43565e2c7a8866cd00d7c18216b74d334'
    }
    
    with open(filepath, 'rb') as fh:
        body = fh.read()
        file = {'upload_file': body}
    root, ext = os.path.splitext(filepath)
    dict_obj = {'headers':myheaders, 'data': body}
    if ext=='.png':
        upurl="http://localhost:3000/uploads.json?filename=image"+ext
        r=requests.post(upurl,**dict_obj)
    elif ext=='.txt':
        upurl="http://localhost:3000/uploads.json?filename=image"+ext
        r=requests.post(upurl,headers=myheaders,files=file)
    return r.text

url="http://localhost:3000/issues/6.json"
wikiurl="http://localhost:3000/projects/the-first/wiki/title1.json"
fileurl="http://localhost:3000/attachments/1"
upurl="http://localhost:3000/uploads.json?filename=image.png"
myheaders = {
    'Content-Type': 'application/octet-stream',
    'X-Redmine-API-Key': '2b002da43565e2c7a8866cd00d7c18216b74d334'
}
filepath='./inu.png'

# by_type={
#     {'.png':{}}
# }

# textdata=upload_redmine(filepath)
# print(textdata)


payload = {
    "wiki_page": {
        "text": "This is a wiki test page.",
    }
    # "issue": {
    #     # "project_id": 1,#プロジェクト選択
    #     # "subject": "apirequests-test5",#チケットの名前
    #     # "status_id": 1,#ステータス
    #     # "tracker_id": 2,#トラッカー
    #     # "priority_id": 1,#優先度
    #     #"assigned_to_id":1,#担当者
    #     # "description": "APIを利用してPythonRequestsからチケットを作成できるかのテスト",#説明
    #     # "done_ratio":20,#進行度
    #     "uploads": [
    #         {
    #             "token": "15.1aba09fc693e46b70462b5ceb5eae57637c5b2cac2f895310910c392f50e29df",
    #             "filename": "image.png",
    #             "content_type": "image/png"
    #         }
    #     ]
    # }
}

#r=requests.post(upurl,headers=myheaders,data=body)
r = requests.put(wikiurl,headers=myheaders,data=json.dumps(payload))

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
期待するコード = 201
if r.status_code != 期待するコード:
       raise RuntimeError(f"{requests.code}")  
print(r.text)



