import imgsim
from django import forms
from .models import Image
from django.conf import settings
import cv2
import numpy as np
from PIL import Image as PILImage


def calculate_distance(path1: str, path2: str) -> float:
    """
    2つの画像のベクトル間の距離を算出する関数
    :param path1: Path for the first image
    :param path2: Path for the second image
    :return: Vector distance between two images
    """
    # pathから画像データを取得
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    # imgsimライブラリで画像をベクトル化
    vtr = imgsim.Vectorizer()
    vec1 = vtr.vectorize(img1)
    vec2 = vtr.vectorize(img2)
    # 2つのベクトル間の距離を算出
    dist = imgsim.distance(vec1, vec2)
    return dist


def return_group(distance: int, previous_image_group: int, max_distance: int) -> int:
    """
    グループの番号を返す関数
    :param distance: Vector distance between two images
    :param previous_image_group: Group of the previous image
    :param max_distance: Maximum distance to be considered as the same group
    :return: Group number of the uploaded image
    """
    if distance <= max_distance:
        print("same: ", previous_image_group)
        print("dist: ", distance)
        return previous_image_group
    else:
        print("next: ", previous_image_group+1)
        print("dist: ", distance)
        return previous_image_group + 1


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        # ユーザーに入力を許可するフィールドをfieldsで指定する
        fields = ("name", "image")

    def save(self, *args, **kwargs):
        obj = super(ImageForm, self).save(commit=False)
        base_dir = str(settings.BASE_DIR)
        # DBにデータが存在するか確認
        if Image.objects.exists():
            # 一つ前の投稿データを取得
            latest_data = Image.objects.latest('created_at')
            # 一つ前の投稿のグループを取得
            latest_group = latest_data.group
            # 初めての画像かを示すflag
            is_first_pic = 0
        else:
            # 画像がまだ登録されていないときはgroup=1
            latest_group = 1
            # 初めての画像かを示すflag
            is_first_pic = 1

        # DBに一旦保存
        obj.group = latest_group
        obj.save()

        # 1つ前の画像データがあれば比較
        if is_first_pic == 0:
            # 一つ前の画像データを取得
            img_latest_path = base_dir + latest_data.image.url
            # 投稿された画像データを取得
            img_uploaded_path = base_dir + obj.image.url
            dist = calculate_distance(path1=img_latest_path, path2=img_uploaded_path)
            group = return_group(distance=dist, previous_image_group=latest_group, max_distance=10)
            obj.group = group
            obj.save()
        return obj
