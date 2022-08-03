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

load_dotenv(verbose=True)
API_KEY = os.environ.get("API_KEY")
SERVER = os.environ.get("SERVER")
PORT = os.environ.get("PORT")

logging.basicConfig(level=logging.DEBUG)
http.client.HTTPConnection.debuglevel = 1


def upload(filepath):
    assert os.path.exists(filepath)
    path, name = os.path.split(filepath)
    base, ext = os.path.splitext(name)

    upurl = f"http://{SERVER}:{PORT}/uploads.json?filepath={name}"

    log.debug(f"upurl {upurl}")

    myheaders = {
        "Content-Type": "application/octet-stream",
        "X-Redmine-API-Key": API_KEY,
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


def ticket_get():
    url = f"http://{SERVER}:{PORT}/issues.json"
    r = requests.get(url)


def ticket_create(filepath):
    with open(filepath, "rb") as fh:
        body = fh.read()
    url = f"http://{SERVER}:{PORT}/issues.json"
    myheaders = {"Content-Type": "application/json", "X-Redmine-API-Key": API_KEY}
    r = requests.post(url, headers=myheaders, data=body)


def ticket_update(filepath, ticketnum):
    with open(filepath, "rb") as fh:
        body = fh.read()
    url = f"http://{SERVER}:{PORT}/issues/{ticketnum}.json"
    myheaders = {"Content-Type": "application/json", "X-Redmine-API-Key": API_KEY}
    r = requests.put(url, headers=myheaders, data=body)


def wiki_create_update(filepath):
    with open(filepath, "rb") as fh:
        jdata = json.load(fh)

    url = f"http://{SERVER}:{PORT}/projects/{jdata['wiki_page']['project']}/wiki/{jdata['wiki_page']['title']}.json"
    myheaders = {"Content-Type": "application/json", "X-Redmine-API-Key": API_KEY}
    r = requests.put(url, headers=myheaders, data=json.dumps(jdata))


def main():
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    text = upload("./inu.jpg")
    print(text)


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
main()
