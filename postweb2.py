# resuests モジュールをインポート
import os
from urllib import response
from urllib.request import urlopen
import dotenv
from matplotlib.font_manager import json_dump, json_load
from matplotlib.pyplot import title
import requests
import json
import logging
import http.client
from dotenv import load_dotenv
from collections import OrderedDict
from ast import literal_eval
from datetime import datetime

load_dotenv(verbose=True)
API_KEY = [os.environ.get("API_KEY1"), os.environ.get("API_KEY2")]
SERVER = [os.environ.get("SERVER1"), os.environ.get("SERVER2")]
PORT = [os.environ.get("PORT1"), os.environ.get("PORT2")]


logging.basicConfig(level=logging.DEBUG)
http.client.HTTPConnection.debuglevel = 1

# 添付ファイルのアップロード
def upload(filepath, servernum=0):
    assert os.path.exists(filepath)
    path, name = os.path.split(filepath)
    base, ext = os.path.splitext(name)

    upurl = f"http://{SERVER[servernum]}:{PORT[servernum]}/uploads.json?filename={name}"

    log.debug(f"upurl {upurl}")

    myheaders = {
        "Content-Type": "application/octet-stream",
        "X-Redmine-API-Key": API_KEY[servernum],
    }
    with open(filepath, "rb") as fh:
        body = fh.read()

    r = requests.post(upurl, headers=myheaders, data=body)
    expected_result = 201
    if r.status_code != expected_result:
        raise RuntimeError(f"{requests.code}")
    log.debug(r.text)
    response_data = literal_eval(r.content.decode("utf8"))

    with open("./token_data.json") as f:
        d_update = json.load(f, object_pairs_hook=OrderedDict)

    d_update[f"data{len(d_update)}"] = response_data
    with open("./token_data.json", "w") as f:
        json.dump(d_update, f, indent=2, ensure_ascii=False)
    return response_data


def download_url(filepath, get=0):
    myheaders = {
        "Content-Type": "application/octet-stream",
        "X-Redmine-API-Key": API_KEY[get],
    }

    res_data = requests.get(filepath, headers=myheaders)
    try:
        contentDisposition = res_data.headers["content-disposition"]
        ATTRIBUTE = "filename="
        local_filename = contentDisposition[contentDisposition.find(ATTRIBUTE) + len(ATTRIBUTE) :]
        local_filename = local_filename.strip('"')
    except:
        contentDisposition = "test"

    contentType = res_data.headers["Content-Type"]
    with open(local_filename, "wb") as aaa:
        aaa.write(res_data.content)
    return local_filename
    # with open(local_filename, "rb") as fh:
    #     body = fh.read()

    # assert os.path.exists(local_filename)
    # path, name = os.path.split(local_filename)
    # base, ext = os.path.splitext(name)

    # myheaders = {
    #     "Content-Type": "application/octet-stream",
    #     "X-Redmine-API-Key": API_KEY[send],
    # }
    # upurl = f"http://{SERVER}:{PORT[send]}/uploads.json?filename={name}"

    # log.debug(f"upurl {upurl}")
    # r = requests.post(upurl, headers=myheaders, data=body)
    # expected_result = 201
    # if r.status_code != expected_result:
    #     raise RuntimeError(f"{requests.code}")
    # log.debug(r.text)
    # response_data = literal_eval(r.content.decode("utf8"))

    # with open("./token_data.json") as f:
    #     d_update = json.load(f, object_pairs_hook=OrderedDict)

    # d_update[f"data{len(d_update)}"] = response_data
    # with open("./token_data.json", "w") as f:
    #     json.dump(d_update, f, indent=2, ensure_ascii=False)


def countticket(getnum=0):
    url = f"http://{SERVER[getnum]}:{PORT[getnum]}/issues.json"
    r = requests.get(url)
    response_data = json.loads(r.text)
    return response_data["issues"][0]["id"]


# 第二引数指定で個別取得、指定なしで一括取得
def ticket_get(portnum=0, ticketnum=0):
    if ticketnum == 0:
        count = countticket(portnum)
    else:
        count = 1

    for page in range(count):
        if ticketnum != 0:
            page = ticketnum - 1

        url = f"http://{SERVER[portnum]}:{PORT[portnum]}/issues/{page+1}.json?limit=100&page={page+1}&include=relations,attachments,journals"
        try:
            r = requests.get(url)
            response_data = json.loads(r.text)
            with open("./issue_get.json", encoding="utf-8") as f:
                dict_data = json.load(f, object_pairs_hook=OrderedDict)

            dict_set = {}
            dict_set = response_data

            # projectid setting
            dict_set["issue"]["project_id"] = dict_set["issue"]["project"]["id"]
            del dict_set["issue"]["project"]

            # statusid setting
            dict_set["issue"]["status_id"] = dict_set["issue"]["status"]["id"]
            del dict_set["issue"]["status"]

            # trackerid setting
            dict_set["issue"]["tracker_id"] = dict_set["issue"]["tracker"]["id"]
            del dict_set["issue"]["tracker"]

            # priorityid setting
            dict_set["issue"]["priority_id"] = dict_set["issue"]["priority"]["id"]
            del dict_set["issue"]["priority"]

            # assigned_to id setting
            dict_set["issue"]["assigned_to_id"] = dict_set["issue"]["assigned_to"]["id"]
            del dict_set["issue"]["assigned_to"]

            # attachments setting
            try:
                dict_set["issue"]["uploads"] = dict_set["issue"]["attachments"]
                # dict_set["issue"]["uploads"][0]["filename"]
                # dict_set["issue"]["uploads"][0]["filename"] = dict_set["issue"]["attachments"][0]["filename"]
                # dict_set["issue"]["uploads"][0]["content_type"] = dict_set["issue"]["attachments"][0]["content_type"]
                # dict_set["issue"]["uploads"][0]["description"] = dict_set["issue"]["attachments"][0]["description"]
                file = download_url(dict_set["issue"]["attachments"][0]["content_url"], portnum)
                text = upload(f"./{file}", 1)
                dict_set["issue"]["uploads"][0]["token"] = text["upload"]["token"]
            except:
                print("添付ファイルなし")

            del dict_set["issue"]["attachments"]

            # data is complete
            dict_data[f"data{len(dict_data)}"] = dict_set
            with open("./issue_get.json", "w", encoding="utf-8") as f:
                json.dump(dict_data, f, indent=2, ensure_ascii=False)
        except:
            print("このチケットは削除されています")


def ticket_copycreate(filepath, num=1, severnum=0):
    with open(filepath, encoding="utf-8") as fh:
        body = json.load(fh, object_pairs_hook=OrderedDict)
    url = f"http://{SERVER[severnum]}:{PORT[severnum]}/issues.json"
    myheaders = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY[severnum],
    }
    for i in range(num):
        for data in range(len(body)):
            jdata = body[f"data{data}"]
            jjdata = json.dumps(jdata)
            r = requests.post(url, headers=myheaders, data=jjdata)


def ticket_update(filepath, ticketnum, severnum=0):
    with open(filepath, "rb") as fh:
        body = fh.read()
    url = f"http://{SERVER[severnum]}:{PORT[severnum]}/issues/{ticketnum}.json"
    myheaders = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY[severnum],
    }
    r = requests.put(url, headers=myheaders, data=body)


def time_entry(filepath, ticketnum, severnum=0):
    with open(filepath, "rb") as fh:
        body = fh.read()
    url = f"http://{SERVER[severnum]}:{PORT[severnum]}/time_entries.json"
    myheaders = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY[severnum],
    }
    r = requests.post(url, headers=myheaders, data=body)


def wiki_create_update(filepath, severnum=0):
    with open(filepath, "rb") as fh:
        jdata = json.load(fh)

    url = f"http://{SERVER[severnum]}:{PORT[severnum]}/projects/{jdata['wiki_page']['project']}/wiki/{jdata['wiki_page']['title']}.json"
    myheaders = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY[severnum],
    }
    r = requests.put(url, headers=myheaders, data=json.dumps(jdata))


def main():
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    # text = ticket_get(ticketnum=5)
    # text = ticket_update("./issue_test.json", 1313, 0)
    text = time_entry("./issue_test.json", 1313, 0)
    # text = ticket_copycreate("./issue_get.json", 1, 0)
    # text = upload("./inu.jpg")
    # text = download_url("http://localhost:3000/attachments/download/5")
    print(text)


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
main()
