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
        base_dir = str(settings.BASE_DIR)
        # DBにデータが存在するか確認
        if Image.objects.exists():
            # 一つ前の投稿データを取得
            latest_data = Image.objects.latest('created_at')
            # 一つ前の投稿のグループを取得
            latest_group = latest_data.group
            # 一つ前の投稿の画像URLを取得し，BASE_DIRと結合
            img_latest_path = base_dir + latest_data.image.url
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

        # 1つ前の画像データがあれば
        if is_first_pic == 0:
            # 一つ前の画像データを取得
            # 画像データをCV2で数値化
            img_latest = cv2.imread(img_latest_path)
            # imgsimライブラリで画像をベクトル化
            vtr = imgsim.Vectorizer()
            vec_img_latest = vtr.vectorize(img_latest)

            # 投稿された画像データを取得
            img_uploaded_path = base_dir + obj.image.url
            img_uploaded = cv2.imread(img_uploaded_path)
            vec_img_uploaded = vtr.vectorize(img_uploaded)
            dist = imgsim.distance(vec_img_latest, vec_img_uploaded)
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
