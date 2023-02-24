from django.db import connection
from synqapp.models import Image
from synqapp.forms import calculate_distance, return_group_for_recalculate_similarity
import cv2
from Synq.settings import BASE_DIR

"""類似度を再計算"""
user_id = 1
data = Image.objects.all().order_by("created_at")

group_list = []

# userとidで絞り込み
# obj = Image.objects.filter(user_id=2, id__lt=47).order_by("created_at").last()
# print(obj.id)

for i, obj in enumerate(data):
    obj.group = 0
    obj.save()

for i, obj in enumerate(data):
    if i == 0:
        group_list.append(1)
        obj.group = 1
        obj.save
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
            group_list.append(prev_group+1)
            continue

    img1_path = str(BASE_DIR) + obj.image.url
    img2_path = str(BASE_DIR) + prev_obj.image.url
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    latest_user_group = prev_obj.group
    print(latest_user_group)
    # グルーピング判定を行い保存
    dist = calculate_distance(img1=img1, img2=img2)
    next_group = max(group_list)
    group = return_group_for_recalculate_similarity(
        previous_image_group=latest_user_group,
        distance=dist, max_distance=15, next_group=next_group
    )
    obj.group = group
    obj.save()
    group_list.append(group)
    # print(group_list)

# for i, obj in enumerate(data):
#     obj.group = group_list[i]
#     obj.save()

# success_url = reverse_lazy('synqapp:image_list')
# return redirect(to=success_url)
