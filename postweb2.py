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

    upurl = f"http://{SERVER}:{PORT}/uploads.json?filename={name}"

    log.debug(f"upurl {upurl}")

    myheaders = {
        "Content-Type": "application/octet-stream",
        "X-Redmine-API-Key": API_KEY,
    }
    with open(filename, "rb") as fh:
        body = fh.read()

    r = requests.post(upurl, headers=myheaders, data=body)
    # Response=urlopen(r)
    # ret=Response.read()
    # print(ret)
    # r = requests.put(wikiurl,headers=myheaders,data=json.dumps(payload))
    expected_result = 201
    if r.status_code != expected_result:
        raise RuntimeError(f"{requests.code}")
    log.debug(r.text)


def ticket_get():
    url = f"http://{SERVER}:{PORT}/issues.json"
    r = requests.get(url)


def ticket_create(filename):
    with open(filename, "rb") as fh:
        body = fh.read()
    url = f"http://{SERVER}:{PORT}/issues.json"
    # fileurl = f"http://{SERVER}:{PORT}/attachments/1"
    myheaders = {"Content-Type": "application/json", "X-Redmine-API-Key": API_KEY}
    r = requests.post(url, headers=myheaders, data=body)


def ticket_update(filename, ticketnum):
    with open(filename, "rb") as fh:
        body = fh.read()
    url = f"http://{SERVER}:{PORT}/issues/{ticketnum}.json"
    myheaders = {"Content-Type": "application/json", "X-Redmine-API-Key": API_KEY}
    r = requests.put(url, headers=myheaders, data=body)

def wiki_create():
    # with open(filename, "rb") as fh:
    #     body = fh.read()
    payload={
        "wiki_page": {
        "title":"title3",
        "text": "This is a wiki test page."
        }
    }
    url = f"http://{SERVER}:{PORT}/projects/the-first/wiki.json"
    myheaders = {"Content-Type": "application/json", "X-Redmine-API-Key": API_KEY}
    r = requests.post(url, headers=myheaders, data=json.dumps(payload))


def main():
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    text = wiki_create()
    print(text)

    # upload('./test.txt')


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
main()
