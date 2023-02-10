import imgsim
from django import forms
from .models import Image
from django.conf import settings
import cv2
import numpy as np
from PIL import Image as PILImage


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        # ユーザーに入力を許可するフィールドをfieldsで指定する
        fields = ("name", "image")

    def save(self, *args, **kwargs):
        obj = super(ImageForm, self).save(commit=False)
        # DBにデータが存在するか確認
        # TODO: DBにファイルがないときの例外処理
        base_dir = str(settings.BASE_DIR)
        if Image.objects.exists():
            # 一つ前の投稿データを取得
            latest_data = Image.objects.latest('created_at')
            # 一つ前の投稿のグループを取得
            latest_group = latest_data.group
            # 一つ前の投稿の画像URLを取得し，BASE_DIRと結合
            img_latest_url = latest_data.image.url
            img_latest_path = base_dir + img_latest_url
            # 画像データをCV2で数値化
            img_latest = cv2.imread(img_latest_path)
            # imgsimライブラリで画像をベクトル化
            vtr = imgsim.Vectorizer()
            vec_img_latest = vtr.vectorize(img_latest)

        obj.group = 15
        obj.save()
        img_upload_path = base_dir + obj.image.url
        img_upload = cv2.imread(img_upload_path)
        vec_img_upload = vtr.vectorize(img_upload)
        dist = imgsim.distance(vec_img_latest, vec_img_upload)
        if dist <= 10:
            group = latest_group
            print("group_same: ", group)
        else:
            group = latest_group + 1
            print("group_next: ", group)
        print("dist: ", dist)
        obj.group = group
        obj.save()
        return obj

        # formの初期値を設定
    # def __init__(self, *args, **kwargs):
    #     super(ImageForm, self).__init__(*args, **kwargs)
    #     # TODO: 画像の類似度を評価
    #     self.instance.group = 13

        # img_pil = PILImage.open(self.instance.image)
        # img = np.asarray(np.array(img_pil))
        # print(img)

    # fieldsにあるフィールドは以下で書き換え可能
    # def clean(self):
    #     self.cleaned_data["name"] = "Mr. Hello"
    #     return self.cleaned_data
