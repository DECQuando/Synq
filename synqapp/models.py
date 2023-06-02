from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

from datetime import datetime
import hashlib
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


def hash_filename(instance, filename):
    current_time = datetime.now()
    pre_hash_name = '%s%s%s' % (instance.name, filename, current_time)
    extension = str(filename).split('.')[-1]
    hs_filename = '%s.%s' % (hashlib.md5(pre_hash_name.encode()).hexdigest(), extension)
    return hs_filename


class Image(models.Model):
    """
    画像データ
    """
    created_at = models.DateTimeField(default=timezone.now, verbose_name='作成日')
    name = models.CharField(max_length=100, verbose_name="名前")
    image = models.ImageField(null=True, blank=True,
                              upload_to=hash_filename,
                              default="media/default_image.png",
                              verbose_name="添付ファイル",
                              validators=[FileExtensionValidator(["jpg", "png"])],
                              )
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(200, 200)],
                               format="JPEG",
                               options={'quality': 85}
                               # qualityはGoogleの方針に従った
                               # cf. https://developers.google.com/speed/docs/insights/OptimizeImages?hl=ja
                               )
    # 一つ前の画像と比較して、類似度を算出し、group番号を付与する
    group = models.IntegerField(null=True, blank=True, verbose_name="グループID")
    # 新たに画像が追加されたグループでベストショットを選出する, それ以外の画像はNoneまたはNullに設定する
    is_best_shot = models.BooleanField(null=True, blank=True, verbose_name="ベストショットか否か",
                                       help_text="ベストショットの画像はTrue, グループ内にTrueは一つのみ")
    edge_sharpness = models.FloatField(null=True, blank=True, verbose_name="エッジの鋭さ", help_text="エッジの鋭さはグループごとに比較する")
    user = models.ForeignKey(
        get_user_model(),
        verbose_name="ユーザー", on_delete=models.CASCADE,
    )

    def __str__(self):
        """管理者画面での表示形式を定義"""
        return "作成日: {} 作成者: {}　グループID: {} ベストショット: {} エッジの鋭さ: {}".format(self.created_at, self.name, self.group,
                                                                                 self.is_best_shot, self.edge_sharpness)
