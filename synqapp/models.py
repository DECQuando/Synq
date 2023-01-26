from django.db import models
from django.utils import timezone


# Create your models here.
class Image(models.Model):
    """
    画像データ
    """
    created_at = models.DateTimeField(default=timezone.now, verbose_name='作成日')
    name = models.CharField(max_length=100)

    def __str__(self):
        return "作成日: {} 作成者: {}".format(self.created_at, self.name)
