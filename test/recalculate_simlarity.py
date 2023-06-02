from django.db import connection
from synqapp.models import Image
from synqapp.forms import calculate_distance, return_group
import cv2
from Synq.settings import BASE_DIR

"""類似度を再計算"""
# userとidで絞り込み
# user_id = 1
# 指定のid以前のデータを取得
# obj = Image.objects.filter(user_id=user_id, id__lt=47).order_by("created_at").last()
# print(obj.id)


def register_group(obj, new_group_num):
    obj.group = new_group_num
    obj.save()


data = Image.objects.all().order_by("created_at")


# グループカラムを初期化
for i, obj in enumerate(data):
    register_group(obj, 0)

for i, obj in enumerate(data):
    if i == 0:
        register_group(obj, 1)
        continue
    # 一つ前のデータを取得
    prev_obj = data[i-1]
    # 全体の最新のグループ番号
    prev_group = prev_obj.group
    # ユーザーが異なる場合
    if obj.user_id != prev_obj.user_id:
        # 現在のユーザーの最後の投稿を取得
        prev_obj = Image.objects.filter(user_id=obj.user_id, id__lt=obj.id).order_by("created_at").last()
        # 現在のユーザーの1番目の投稿データの場合、全体の最新のグループ番号に1足す
        if prev_obj is None:
            register_group(obj, prev_group+1)
            continue

    # 類似度を計算
    img1_path = str(BASE_DIR) + obj.image.url
    img2_path = str(BASE_DIR) + prev_obj.image.url
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    latest_user_group = prev_obj.group
    # print(latest_user_group)
    # グルーピング判定を行い保存
    dist = calculate_distance(img1=img1, img2=img2)
    # next_group = max(group_list)
    group = return_group(
        previous_image_group=latest_user_group,
        distance=dist, max_distance=15
    )
    register_group(obj, group)
