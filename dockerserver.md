# docker　redmineの開発サーバー立てる方法

## 1.  ローカルでディレクトリ作成
 * 構成内容

        適当な場所
            └─my_prot01
                └─docker-compose.yml
            └─data
                └─my_prot01
                └─db

* docker-compose.ymlの内容


``` 
version: '3.9'
services:
  redmine:
    image: redmine:passenger
    container_name: redmine
    ports:
      - 3000:3000
    environment:
      TZ: Asia/Tokyo
      REDMINE_DB_MYSQL: mysql
      REDMINE_DB_DATABASE: redmine
      REDMINE_DB_USERNAME: redmine
      REDMINE_DB_PASSWORD: redmine
      REDMINE_DB_ENCODING: utf8
    depends_on:
      - mysql
    restart: always
    volumes:
      - ../data/my_prot01/redmine/files:/usr/src/redmine/files
      - ../data/my_prot01/redmine/redmine/log:/usr/src/redmine/log
      - ../data/my_prot01/redmine/plugins:/usr/src/redmine/plugins
      - ../data/my_prot01/redmine/redmine/public/themes:/usr/src/redmine/public/themes

  mysql:
    image: mysql:5.7
    container_name: mysql
    restart: always
    environment:
      TZ: Asia/Tokyo
      MYSQL_ROOT_PASSWORD: devops
      MYSQL_DATABASE: redmine
      MYSQL_USER: redmine
      MYSQL_PASSWORD: redmine
    volumes:
      - ../data/db:/var/lib/mysql
    command: mysqld --character-set-server=utf8 --collation-server=utf8_unicode_ci
```

## 2.  docker-composeコマンド実行
    docker-compose.ymlの入っているmy_prot01のアドレスでコマンド実行
    例）C:\docker\my_prot01> docker-compose up -d


## 3.  Redmineアクセス
``` http://localhost:3000```にアクセス
ログインIDパスワードはadminがデフォルトで設定されています。