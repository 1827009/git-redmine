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
API_KEY1 = os.environ.get("API_KEY1")
SERVER = os.environ.get("SERVER")
PORT1 = os.environ.get("PORT1")

logging.basicConfig(level=logging.DEBUG)
http.client.HTTPConnection.debuglevel = 1


def DownloadFile(url):

    DOWNLOAD_SAVE_DIR = os.getenv("DOWNLOAD_SAVE_DIR")
    myheaders = {
        "Content-Type": "image/jpeg",
        "X-Redmine-API-Key": API_KEY1,
    }
    response = requests.get(url, headers=myheaders)

    responseurl = response.url
    print(responseurl)
    # ★ポイント3
    contentType = response.headers["Content-Type"]

    response = requests.get(responseurl)
    contentType = response.headers["Content-Type"]

    contentDisposition = response.headers["content-disposition"]
    ATTRIBUTE = "filename="
    fileName = contentDisposition[contentDisposition.find(ATTRIBUTE) + len(ATTRIBUTE) :]

    # ★ポイント4
    saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") + fileName
    saveFilePath = os.path.join(DOWNLOAD_SAVE_DIR, saveFileName)
    with open(saveFilePath, "wb") as saveFile:
        saveFile.write(response.content)


def get_attach():
    upurl = f"http://{SERVER}:{PORT1}/uploads.json"


def upload(filepath):
    assert os.path.exists(filepath)
    path, name = os.path.split(filepath)
    base, ext = os.path.splitext(name)

    upurl = f"http://{SERVER}:{PORT1}/uploads.json?filename={name}"

    log.debug(f"upurl {upurl}")

    myheaders = {
        "Content-Type": "application/octet-stream",
        "X-Redmine-API-Key": API_KEY1,
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


def upload_url(filepath):
    myheaders = {
        "Content-Type": "image/jpeg",
        "X-Redmine-API-Key": API_KEY1,
    }

    res_data = requests.get(filepath, headers=myheaders)
    local_filename = filepath.split("/")[-1]
    with open(local_filename, "wb") as aaa:
        aaa.write(res_data.content)

    with open(local_filename, "rb") as fh:
        body = fh.read()

    assert os.path.exists(local_filename)
    path, name = os.path.split(local_filename)
    base, ext = os.path.splitext(name)

    upurl = f"http://{SERVER}:{PORT1}/uploads.json?filename={name}"

    log.debug(f"upurl {upurl}")
    myheaders = {
        "Content-Type": "application/octet-stream",
        "X-Redmine-API-Key": API_KEY1,
    }
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


def ticket_get():
    url = f"http://{SERVER}:{PORT1}/issues.json"
    r = requests.get(url)
    response_data = json.loads(r.text)
    with open("./issue_get.json", encoding="utf-8") as f:
        dict_data = json.load(f, object_pairs_hook=OrderedDict)

    for data in response_data["issues"]:
        dict_set = {}
        dict_set["issue"] = data

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

        dict_data[f"data{len(dict_data)}"] = dict_set

    with open("./issue_get.json", "w", encoding="utf-8") as f:
        json.dump(dict_data, f, indent=2, ensure_ascii=False)


def ticket_create(filepath):
    with open(filepath, "rb") as fh:
        body = json.load(fh, object_pairs_hook=OrderedDict)
    url = f"http://{SERVER}:{PORT1}/issues.json"
    myheaders = {"Content-Type": "application/json", "X-Redmine-API-Key": API_KEY1}
    for data in range(len(body)):
        jdata = body[f"data{data}"]
        r = requests.post(url, headers=myheaders, data=json.dumps(jdata))


def ticket_update(filepath, ticketnum):
    with open(filepath, "rb") as fh:
        body = fh.read()
    url = f"http://{SERVER}:{PORT1}/issues/{ticketnum}.json"
    myheaders = {"Content-Type": "application/json", "X-Redmine-API-Key": API_KEY1}
    r = requests.put(url, headers=myheaders, data=body)


def wiki_create_update(filepath):
    with open(filepath, "rb") as fh:
        jdata = json.load(fh)

    url = f"http://{SERVER}:{PORT1}/projects/{jdata['wiki_page']['project']}/wiki/{jdata['wiki_page']['title']}.json"
    myheaders = {"Content-Type": "application/json", "X-Redmine-API-Key": API_KEY1}
    r = requests.put(url, headers=myheaders, data=json.dumps(jdata))


def main():
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    # text = ticket_get()
    # text = ticket_create("./issue_get.json")
    # text = upload("./inu.jpg")
    text = upload_url("http://localhost:3000/attachments/download/5/inu.jpg")
    # text = DownloadFile("http://localhost:3000/attachments/download/5/inu.jpg")
    print(text)


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
main()
