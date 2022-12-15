#マニュアル
<dl>
<dt>.env</dt>
<dd>
設定用ファイル。

API_KEY1・API_KEY2：RedmineのAPIKey
SERVER1・SERVER2：サーバーのIPアドレス
PORT1・PORT2：サーバーのポート番号
</dd>
<dt>〇〇_get.json</dt>
<dd>取得チケットデータ格納用。getの際にcreateしやすい形に変形させているため、手動でチケットデータを作る際には参考にしてください</dd>
<dt>postweb2.py</dt>
<dd>メインプログラム。下記参照</dd>
<dt>requirements.txt</dt>
<dd>ダウンロード用</dd>
<dt>test.txt</dt>
<dd>テキストファイル添付テスト用</dd>
<dt>token_data.json</dt>
<dd>添付ファイルアップロード時のトークン格納用</dd>
</dl>


##事前準備
Redmine側の設定、APIタブの内容にすべてチェック
Redmine側のAPIアクセスキーを作成
.envファイルに作成したキー、ポートなどを設定


##postweb2.py使い方
サーバーの指定は.envで指定したSERVERやPORTの番号(0 or 1)で送受信を設定してください
<dl>
  <dt>〇〇_get(保存するjsonファイル, 呼び出すitemの名前, サーバーの指定)</dt>
  <dd>指定したfileに取得したitemをjsonで保存します。呼び出すitemの名前を指定しなければすべてを呼び出し、保存します</dd>

  <dt>〇〇_create(jsonデータ, サーバーの指定)</dt>
  <dd>指定したフォルダのjsonでRedmineにitemを作成します。</dd>

  <dt>ticket_create(jsonデータ, プロジェクトの名前, サーバーの指定)</dt>
  <dd>チケットを作成します。プロジェクトの名前を指定するとあらゆるチケットをそのプロジェクトに作成します。指定しない場合、チケットデータ内のprojectnameと同一の名前のプロジェクトに作成されます</dd>
  
  <dt>ticket_update(チケットのjsonデータ, 送るプロジェクト, サーバーの指定)</dt>
  <dd>チケットを更新します。ticket_createのほぼコピペです</dd>
  
  <dt>upload(添付ファイルのパス,サーバーの指定)</dt>
  <dd>添付ファイルをアップロードしてトークンを生成します。token_data.jsonに格納。基本的に〇〇_getに内蔵されているため気にしなくていいです</dd>
</dl> 
