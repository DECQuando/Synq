from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        # ユーザーに入力を許可するフィールドをfieldsで指定する
        fields = ("name", "image")

        # formの初期値を設定
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.instance.group = 13

    # fieldsにあるフィールドは以下で書き換え可能
    # def clean(self):
    #     self.cleaned_data["name"] = "Mr. Hello"
    #     return self.cleaned_data
