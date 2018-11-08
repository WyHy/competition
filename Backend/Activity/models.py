from django.db import models

# Create your models here.
from PathologyType.models import Type
from Profile.models import Profile
from TIFF.models import Image


class Answer(models.Model):
    """
    活动竞猜信息观众答案
    """

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="关联病理图像")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="关联用户")
    answer = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="用户答案")

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.profile.nickname) + "-" + str(self.answer.name)

    class Meta:
        verbose_name = u'竞猜信息'
        verbose_name_plural = u'竞猜信息'
