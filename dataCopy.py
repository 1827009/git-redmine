import urllib.request, urllib.error
import json
import requests

# 個人設定画面に表示されているAPIキー
api_key = '2b002da43565e2c7a8866cd00d7c18216b74d334'
# まず、添付ファイルのアップロードを実行
f = open('inu.jpg', 'rb')
img = f.read()
f.close()
url = 'http://localhost:3000/uploads.json'
request = urllib.request.Request(url, data=img)
request.add_header('Content-Type', 'application/octet-stream')
request.add_header('X-Redmine-API-Key', api_key)
request.get_method = lambda: 'POST'
response = urllib.request.urlopen(request)
ret = response.read()
# レスポンスからtokenを取得
retjson = json.loads(ret)
token = retjson[u'upload'][u'token']
print(token)
# 登録用のデータ
issue = {}
issue[u'project_id'] = u'test_project'
issue[u'tracker_id'] = 3
issue[u'subject'] = u'JSONからの自動登録テスト'
issue[u'description'] = u'JSONから登録してみます。'
imgdata = {}
imgdata[u'token'] = token
imgdata[u'filename'] = u'Lenna.jpg'
imgdata[u'description'] = u'添付ファイルサンプル'
imgdata[u'content_type'] = u'image/jpg'
issue[u'uploads'] = [imgdata]
data = {}
data[u'issue'] = issue
# JSON形式の文字列を取得
jsonstr = json.dumps(data)
# APIのURL
# 今回、RedmineのURLはhttp://192.168.1.102/redmine/
# サブディレクトリで公開している
# jsonの場合は、拡張子に「json」を指定
url = 'http://localhost:3000/projects/the-first/wiki/Wiki.json'
# Content-Type:application/json
# X-Redmine-API-Key:[APIキー]
# method:post
myheaders = {
    'Content-Type': 'application/json',
    'X-Redmine-API-Key': '2b002da43565e2c7a8866cd00d7c18216b74d334'
}
r=requests.post(url,headers=myheaders,data=jsonstr)
# request = urllib.request.Request(url, data=jsonstr)
# request.add_header('Content-Type', 'application/json')
# request.add_header('X-Redmine-API-Key', api_key)
# request.get_method = lambda: 'POST'

# 登録実行
response = urllib.request.urlopen(request)
ret = response.read()
print ('Response:', ret)
