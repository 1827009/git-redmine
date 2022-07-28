# resuests モジュールをインポート
from urllib import response
from urllib.request import urlopen
from matplotlib.font_manager import json_dump
import requests
import json
import logging
import http.client

logging.basicConfig(level=logging.DEBUG)
http.client.HTTPConnection.debuglevel = 1

url="http://localhost:3000/issues/6.json"
wikiurl="http://localhost:3000/projects/the-first/wiki/Wiki.json"
fileurl="http://localhost:3000/attachments/1"
upurl="http://localhost:3000/uploads.json?filename=image.png"
myheaders = {
    'Content-Type': 'application/octet-stream',
    'X-Redmine-API-Key': '2b002da43565e2c7a8866cd00d7c18216b74d334'
}
with open('./inu.png', 'rb') as fh:
    body = fh.read()
    file = {'upload_file': body}

#file = {'upload_file': open('./test.txt', 'rb')}
# f = open('./inu.png', 'rb')
# img = f.read()
# f.close()

# payload = {
#     #  "wiki_page": {
#     #     "title":"title2",
#     #     "text": "This is a wiki test page.",
#     # }
#     "issue": {
#         # "project_id": 1,#プロジェクト選択
#         # "subject": "apirequests-test5",#チケットの名前
#         # "status_id": 1,#ステータス
#         # "tracker_id": 2,#トラッカー
#         # "priority_id": 1,#優先度
#         #"assigned_to_id":1,#担当者
#         # "description": "APIを利用してPythonRequestsからチケットを作成できるかのテスト",#説明
#         # "done_ratio":20,#進行度
#         "uploads": [
#             {
#                 "token": "15.1aba09fc693e46b70462b5ceb5eae57637c5b2cac2f895310910c392f50e29df",
#                 "filename": "image.png",
#                 "content_type": "image/png"
#             }
#         ]
#     }
# }

r=requests.post(upurl,headers=myheaders,data=body)
# Response=urlopen(r)
# ret=Response.read()
# print(ret)
# r = requests.put(wikiurl,headers=myheaders,data=json.dumps(payload))

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
期待するコード = 201
if r.status_code != 期待するコード:
       raise RuntimeError(f"{requests.code}")  
print(r.text)
