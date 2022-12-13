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

# 取得したデータを書き込むjsonファイルを指定, projectname指定で個別取得、未指定で一括取得 送信先に同名のプロジェクトがある場合作成されない
def project_get(filepath, projectname="", severnum=0):
    if projectname == "":
        url = f"http://{SERVER[severnum]}:{PORT[severnum]}/projects.json?key={API_KEY[severnum]}"
    else:
        url = f"http://{SERVER[severnum]}:{PORT[severnum]}/projects/{projectname}.json?key={API_KEY[severnum]}"
    try:
        r = requests.get(url)
        response_data = json.loads(r.text)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)
        return response_data

    except:
        print("プロジェクトは存在しません")

# 作成するjsonファイルを指定
def project_upload(projectpash, severnum=0):
    with open(projectpash, encoding="utf-8") as f:
        dict_data = json.load(f, object_pairs_hook=OrderedDict)

    url = f"http://{SERVER[severnum]}:{PORT[severnum]}/projects.json?key={API_KEY[severnum]}"

    myheaders = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY[severnum],
    }
    
    r = requests.post(url, headers=myheaders, data=json.dumps(dict_data))
    
    
# 取得したデータを書き込むjsonファイルを指定, ticketname指定で個別取得、指定なしで一括取得, projectname指定でプロジェクト単位で取得、指定なしで一括取得
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

        for i in range(indcount):
            data={}
            data["issue"]=index_data["issues"][i]

            # projectid setting
            try:
                data["issue"]["project_id"] = data["issue"]["project"]["id"]
                del data["issue"]["project"]
            except:
                print("projectなし")

            # statusid setting
            try:
                data["issue"]["status_id"] = data["issue"]["status"]["id"]
                del data["issue"]["status"]
            except:
                print("statusなし")

            # trackerid setting
            try:
                data["issue"]["tracker_id"] = data["issue"]["tracker"]["id"]
                del data["issue"]["tracker"]
            except:
                print("trackerなし")

            # priorityid setting
            try:
                data["issue"]["priority_id"] = data["issue"]["priority"]["id"]
                del data["issue"]["priority"]
            except:
                print("priorityidなし")

            # assigned_to id setting
            try:
                data["issue"]["assigned_to_id"] = data["issue"]["assigned_to"]["id"]
                del data["issue"]["assigned_to"]
            except:
                print("assignedなし")

            # attachments setting
            try:
                data["issue"]["uploads"] = data["issue"]["attachments"]
                # dict_set[i]["uploads"][0]["filename"]
                # dict_set[i]["uploads"][0]["filename"] = dict_set["issue"]["attachments"][0]["filename"]
                # dict_set[i]["uploads"][0]["content_type"] = dict_set["issue"]["attachments"][0]["content_type"]
                # dict_set[i]["uploads"][0]["description"] = dict_set["issue"]["attachments"][0]["description"]
                file = download_url(data["issue"]["attachments"][0]["content_url"], portnum)
                text = upload(f"./{file}", 1)
                data["issue"]["uploads"][0]["token"] = text["upload"]["token"]
                del data["issue"]["attachments"]
            except:
                print("添付ファイルなし")

            dict_data[f"data{offset*100+i}"]=data
        
        if indcount>=100:
            offset+=1
            continue
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dict_data, f, indent=2, ensure_ascii=False)
            break
    
    return dict_data
    
# 作成するjsonファイルを指定, projectname指定でチケットのproject_idを書き換えてサーバーに作成、未指定でidに合わせたプロジェクトに作成
def ticket_create(filepath, projectname="", severnum=0):

    with open(filepath, encoding="utf-8") as fh:
        body = json.load(fh, object_pairs_hook=OrderedDict)
    url = f"http://{SERVER[severnum]}:{PORT[severnum]}/issues.json"
    myheaders = {
        "Content-Type": "application/json",
        "X-Redmine-API-Key": API_KEY[severnum],
    }
    for data in range(len(body)):
        jdata = body[f"data{data}"]
        if projectname!="":
            p=project_get(projectname, severnum)
            jdata["issue"]["project_id"]=p['project']["id"]
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

# 取得したデータを書き込むjsonファイルを指定, wikiname指定で個別取得、指定なしで一括取得
def wiki_get(filepath, projetname, wikiname="", severnum=0):
    if wikiname!="":
        wikiname=f"/{wikiname}"

    indexurl = f"http://{SERVER[severnum]}:{PORT[severnum]}/projects/{projetname}/wiki{wikiname}.json?key={API_KEY[severnum]}&include=relations,attachments,journals"
    try:
        r = requests.get(indexurl)
        response_data = json.loads(r.text)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)

        return response_data
    except:
        print("そのWikiは存在しません")

# 作成ができないバグ発生中
def wiki_create(filepath, projectname, severnum=0):
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
    # text = ticket_get("./issue_get.json")
    # text=ticket_create("foo", "./issue_get.json")
    # text = ticket_create("./issue_get.json", "foo")
    # text = ticket_update("./issue_test.json", 11, 0)
    # text = time_entry("./issue_test.json", 1313, 0)
    # text = download_url("http://localhost:3000/attachments/download/5")
    # text = wiki_create_update("./wiki_test.json")
    # text = wiki_get("./wiki_get.json", "foo")
    text = wiki_create("./wiki_get.json", "foo", 1)
    # text = project_get()
    # text = project_upload("./project_get.json", 1)
    print(text)


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
main()
