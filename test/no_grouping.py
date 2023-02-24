from django.db import connection
from synqapp.models import Image

# グルーピングなしのアルバム表示するときのテストコード

data = Image.objects.filter(user_id=1).order_by("created_at")
if data.exists():
    print("yes")

a = [0, 1, 2, 3]
for i in range(len(a)):
    print(a[i])
    if a[i] == 2:
        if a[i] == 2:
            print("this")
            # continueは最上階のforloopまで抜ける。
            continue
    print("-------")
