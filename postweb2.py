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

# プロジェクト名指定でプロジェクトのjson、未指定でプロジェクトの一覧を取得
def project_get(projectname="", portnum=0):
    if projectname == "":
        url = f"http://{SERVER[portnum]}:{PORT[portnum]}/projects.json?key={API_KEY[portnum]}"
    else:
        url = f"http://{SERVER[portnum]}:{PORT[portnum]}/projects/{projectname}.json?key={API_KEY[portnum]}"
    try:
        r = requests.get(url)
        response_data = json.loads(r.text)
        
        with open("./project_get.json", "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)
        return response_data['projects']

    except:
        print("プロジェクトは存在しません")

# 作成ができないバグ発生中
def project_upload(projectpash, severnum=0):
    with open(projectpash, encoding="utf-8") as f:
        dict_data = json.load(f, object_pairs_hook=OrderedDict)

    url = f"http://{SERVER[severnum]}:{PORT[severnum]}/projects.json?key={API_KEY[severnum]}"

    myheaders = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY[severnum],
    }
    
    r = requests.post(url, headers=myheaders, data=json.dumps(dict_data))
    

# 第二引数指定で個別取得、指定なしで一括取得
def ticket_get(filepath, ticketname="", projectname="", portnum=0):
    
    offset=0
    dict_data={}
    while True:
        if ticketname!="":
            ticketname=f"&subject={ticketname}"
        if projectname!="":
            projectname=f"&project_id={projectname}"

        index_url = f"http://{SERVER[portnum]}:{PORT[portnum]}/issues.json?offset={offset*100}&limit=100{projectname}{ticketname}&status_id=*&sort=id&include=relations,attachments,journals"
        r = requests.get(index_url)
        index_data = json.loads(r.text)
        indcount = len(index_data["issues"])

        try:
            a= index_data['issues']
            b= dict_data['issues']
            b.extend(a)
            dict_data['issues']=b
        except:
            dict_data=index_data
            print("空のファイル?")
        
        
        if indcount>=100:
            offset+=1
            continue
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dict_data, f, indent=2, ensure_ascii=False)
            break
    
# 作成ができないバグ発生中。
def ticket_create(projectname, filepath, severnum=0):
    with open(filepath, encoding="utf-8") as fh:
        body = json.load(fh, object_pairs_hook=OrderedDict)

    url = f"http://{SERVER[severnum]}:{PORT[severnum]}/projects/{projectname}/wiki.json?key={API_KEY[severnum]}"

    myheaders = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY[severnum],
    }
    
    r = requests.post(url, headers=myheaders, data=json.dumps(body))

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


def wiki_get(filepath, projetname, wikiname="", portnum=0):

        project=project_get(portnum)
        if wiki_create!="":
            indexurl = f"http://{SERVER[portnum]}:{PORT[portnum]}/projects/{projetname}/wiki/{projetname}.json?key={API_KEY[portnum]}&include=relations,attachments,journals"
        else:
            indexurl = f"http://{SERVER[portnum]}:{PORT[portnum]}/projects/{projetname}/wiki/index.json?key={API_KEY[portnum]}&include=relations,attachments,journals"
        try:

            r = requests.get(indexurl)
            response_data = json.loads(r.text)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(response_data, f, indent=2, ensure_ascii=False)

            return response_data
        except:
            print("そのWikiは存在しません")

# 作成ができないバグ発生中
def wiki_create(projectname, filepath, severnum=0):
    with open(filepath, encoding="utf-8") as fh:
        body = json.load(fh, object_pairs_hook=OrderedDict)

    url = f"http://{SERVER[severnum]}:{PORT[severnum]}/projects/{projectname}/wiki.json?key={API_KEY[severnum]}"

    myheaders = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY[severnum],
    }
    
    r = requests.post(url, headers=myheaders, data=json.dumps(body))

def wiki_create_update(filepath, severnum=0):
    with open(filepath, "rb") as fh:
        jdata = json.load(fh)

    #url = f"http://{SERVER[severnum]}:{PORT[severnum]}/projects/{jdata['wiki_page']['project']}/wiki/{jdata['wiki_page']['title']}.json"
    url = f"http://{SERVER[severnum]}:{PORT[severnum]}/projects/foo/wiki/{jdata['wiki_page']['title']}.json?key={API_KEY[severnum]}"
    myheaders = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY[severnum],
    }
    r = requests.post(url, headers=myheaders, data=json.dumps(jdata))


def main():
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    # text = upload("./inu.jpg")
    text = ticket_get("./issue_get.json", "testチケット1-2")
    # text = ticket_copycreate("./issue_get.json")
    # text = ticket_update("./issue_test.json", 11, 0)
    # text = time_entry("./issue_test.json", 1313, 0)
    # text = download_url("http://localhost:3000/attachments/download/5")
    # text = wiki_create_update("./wiki_test.json")
    # text = wiki_get("./wiki_get.json", "foo")
    # text = wiki_create("foo", "./wiki_get.json", 0)
    # text = project_get()
    # text = project_upload("./project_get.json", 0)
    print(text)


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
main()
