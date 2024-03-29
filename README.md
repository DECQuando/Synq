# このコードについて

# 使い方

## コンソールからDBの値を取得
[Djangoで実行されたクエリを確認したい(connection.queries)](https://www.denzow.me/entry/2018/06/13/234953)

```python
from django.db import connection
from synqapp.models import Image

Image.objects.filter(id=1)
# <QuerySet [<Image: 作成日: 2023-01-26 04:05:21+00:00 作成者: admin　グループID: 1>]>
```

## コードのフォーマット
Pycharmでコードのフォーマットをするには、
```bash
command + option + L
```
- 参考: 
[【PyCharm】ファイル保存時に自動フォーマット（整形）](https://sleepless-se.net/2021/12/04/pycharm-auto-format/)

## requirements.txt
### 生成方法
```bash
pip freeze > requirements.txt
```

### インストール方法
```bash
pip install -r requirements.txt
```


## migrate
### migrationファイルの作成
```bash
python manage.py makemigrations
```

### マイグレーション
```bash
python manage.py migrate
```


## `SECRET_KEY`の生成方法

ターミナルで以下を実行。
```bash
cd Synq

touch get_random_secret_key.py 
```

`get_random_secret_key.py`に以下をペーストする。

```python
from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
text = 'SECRET_KEY = \'{0}\''.format(secret_key)
print(text)
```

ターミナルで以下を実行する。

```bash
python3 get_random_secret_key.py > local_settings.py

cat local_settings.py
# SECRET_KEY = '******************'と表示されるはず
```

### 参考
- [DjangoのSECRET_KEYをバージョン管理対象外にする](https://qiita.com/haessal/items/abaef7ee4fdbd3b218f5)
- [【Django】SECRET_KEYなどの機密情報を別ファイルで管理](https://chigusa-web.com/blog/django-secret/)



## Dockerを用いたビルド
### Prerequisite
- Docker

### ビルド方法
事前にDockerを立ち上げておく。
以下 $BASE_DIRはベースディレクトリのPATHを表す(例: ~/Synq/)。
```bash
cd $BASE_DIR

# ビルド(初回のみ)
docker build -t synq:1.0 $BASE_DIR

# 立ち上げ
docker run -it --rm -p 8000:8000 -v $BASE_DIR:/root/Synq \
  --name Synq synq:1.0 /bin/bash
# dockerコンテナの中で#rootとしてターミナルが立ち上がる
# そのターミナル内で以下を実行
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:800
# Ctrl+Cでサーバーを停止、Ctrl+Dでターミナルを抜けられる。
```

### 参考
- [Django Documentation Settings ALLOWED_HOST](https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts)
- [Docker(Docker-Compose)】Python,Djangoの開発・本番環境構築【Postgres,Gunicorn,Nginx利用】](https://tomato-develop.com/docker-dockercompose-python-django-postgresql-gunicorn-nginx-how-to-build-development-and-production-environment/)
- [現場で使える Django の教科書《基礎編》](https://amzn.asia/d/g1zXfkl)