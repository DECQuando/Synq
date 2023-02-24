from django.db import connection
from synqapp.models import Image

# グルーピングなしのアルバム表示するときのテストコード

data = Image.objects.filter(user_id=1).order_by("created_at")
if data.exists():
    print("yes")
