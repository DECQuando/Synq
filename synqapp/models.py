from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


# Create your models here.
class Image(models.Model):
    """
    画像データ
    """
    created_at = models.DateTimeField(default=timezone.now, verbose_name='作成日')
    name = models.CharField(max_length=100, verbose_name="名前")
    image = models.ImageField(null=True, blank=True,
                              # upload_to="media",
                              # upload_to="uploads/%Y/%m/%d/",
                              verbose_name="添付ファイル",
                              validators=[FileExtensionValidator(["jpg", "png"])],
                              )

    def __str__(self):
        """管理者画面での表示形式を定義"""
        return "作成日: {} 作成者: {}".format(self.created_at, self.name)
