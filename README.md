#マニュアル
.env　設定用ファイル
copy.py 試作用の為ツール本体には関係ないです
issue_get.json 取得チケットデータ格納用
issue_test.json チケット作成のデータを自作する用
postweb2.py メインプログラム
requirements.txt　ダウンロード用
test.txt  テキストファイル添付テスト用
token_data.json　添付ファイルアップロード時のトークン格納用
wiki_test.json　wiki作成用データ



##事前準備
Redmine側の設定、APIタブの内容にすべてチェック
Redmine側のAPIアクセスキーを作成
.envファイルに作成したキー、ポートなどを設定


##postweb2.py使い方

###〇〇_get(保存するファイル, 呼び出すitemの名前, port番号)
指定したfileに取得したitemをjsonで保存します。
呼び出すitemの名前を指定しなければすべてを呼び出し、保存します

###〇〇_create()
指定したフォルダのjsonでRedmineにitemを作成するはずでした。
現状バグで一切動かなくなっているため、folk元のリポジトリを参考にしてください

###upload(添付ファイルのパス,サーバーの指定)
添付ファイルをアップロードします
アップロード時にtoken_data.jsonに格納

###download_url()
ticket_get()内で呼び出す関数


###countticket()
ticket_get()内で呼び出す関数

###ticket_update(チケットのjsonデータ,チケット番号,サーバーの指定）
チケットの更新用

###time_entry(jsonデータ,サーバーの指定)
作業履歴作成用（まだ制作中）

###wiki_create_update(jsonデータ,サーバーの指定)
wiki更新用(まだ制作中）


