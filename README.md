.env　設定用ファイル
copy.py 試作用の為ツール本体には関係ないです
issue_get.json 取得チケットデータ格納用
issue_test.json チケット作成のデータを自作する用
postweb2.py メインプログラム
requirements.txt　ダウンロード用
test.txt  テキストファイル添付テスト用
token_data.json　添付ファイルアップロード時のトークン格納用
wiki_test.json　wiki作成用データ



事前準備
Redmine側の設定、APIタブの内容にすべてチェック
Redmine側のAPIアクセスキーを作成
.envファイルに作成したキー、ポートなどを設定


postweb2.py使い方

upload(添付ファイルのパス,サーバーの指定)
添付ファイルをアップロードします
アップロード時にtoken_data.jsonに格納

download_url()
ticket_get()内で呼び出す関数


countticket()
ticket_get()内で呼び出す関数

ticket_get(サーバーの指定,チケット番号)
チケット番号を指定時、個別で取得
チケット情報を取得し、issue_get.jsonに格納


ticket_copycreate(チケットのjsonデータ,num, サーバーの指定)
jsonデータは基本的にissue_get.jsonを指定、numは大量に同じチケットを作成したいときのみ入力

ticket_update(チケットのjsonデータ,チケット番号,サーバーの指定）
チケットの更新用

time_entry(jsonデータ,サーバーの指定)
作業履歴作成用（まだ制作中）

wiki_create_update(jsonデータ,サーバーの指定)
wiki更新用(まだ制作中）


