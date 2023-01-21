# このコードについて

# 使い方
## requirements.txt
### 生成方法
```bash
pip freeze > requirements.txt
```

### インストール方法
```bash
pip install -r requirements.txt
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



