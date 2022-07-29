# resuests モジュールをインポート
import os
from urllib import response
from urllib.request import urlopen
import dotenv
from matplotlib.font_manager import json_dump
import requests
import json
import logging
import http.client
from dotenv import load_dotenv

load_dotenv(verbose=True)
API_KEY = os.environ.get("API_KEY")
SERVER = os.environ.get("SERVER")
PORT = os.environ.get("PORT")

logging.basicConfig(level=logging.DEBUG)
http.client.HTTPConnection.debuglevel = 1
def upload(filename):
    assert os.path.exists(filename)
    path, name = os.path.split(filename)
    base, ext = os.path.splitext(name)

    url = f"http://{SERVER}:{PORT}/issues/6.json"
    wikiurl = f"http://{SERVER}:{PORT}/projects/the-first/wiki/Wiki.json"
    fileurl = f"http://{SERVER}:{PORT}/attachments/1"
    upurl = f"http://{SERVER}:{PORT}/uploads.json?filename={name}"

    log.debug(f"upurl {upurl}")

    myheaders = {
        'Content-Type': 'application/octet-stream',
        'X-Redmine-API-Key': API_KEY
    }
    with open(filename, 'rb') as fh:
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
    r = requests.post(upurl,headers=myheaders,data=body)
    # Response=urlopen(r)
    # ret=Response.read()
    # print(ret)
    # r = requests.put(wikiurl,headers=myheaders,data=json.dumps(payload))
    expected_result = 201
    if r.status_code != expected_result:
        raise RuntimeError(f"{requests.code}")  
    log.debug(r.text)

def main():
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    upload('./test.txt')

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
main()    