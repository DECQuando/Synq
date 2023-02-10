from django import forms
from django.db.models import Max

from .models import Image
from Synq.settings import BASE_DIR

import cv2
import numpy as np
from PIL import Image as PILImage
from pathlib import Path


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        # ユーザーに入力を許可するフィールドをfieldsで指定する
        fields = ("name", "image")

    def save(self, *args, **kwargs):
        obj = super(ImageForm, self).save(commit=False)
        obj.group = 13

        # 画像のBASE_DIRからの相対パスを取得(first forward slashを除去)
        image_relative_path = Path(obj.image.url.replace('/', '', 1))
        image_absolute_path = BASE_DIR / image_relative_path
        image = cv2.imread(str(image_absolute_path))
        obj.blur = self.variance_of_laplacian(image)

        obj.save()
        self.select_best_shot(obj.group)
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

    def select_best_shot(self, group_id):
        obj = Image.objects.filter(group=group_id)

        # グループ中のベストショットの有無を確認(新規グループ作成時は存在しないため分岐必須)
        if obj.filter(is_best_shot=True).exists():
            # 元々のベストショットのフラグを消去する
            obj.filter(is_best_shot=True).update(is_best_shot=None)

        # 新しくベストショットのフラグを付与する
        # TODO: ベストショット選出アルゴリズムを実装し最大idの画像にフラグを付与する箇所を置き換える
        obj_new_best_shot = obj.get(id=obj.aggregate(Max('id'))['id__max'])
        obj_new_best_shot.is_best_shot = True
        obj_new_best_shot.save()

    def variance_of_laplacian(self, image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()
