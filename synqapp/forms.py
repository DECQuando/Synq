from django import forms
from .models import Image
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
        obj.group = 13
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
