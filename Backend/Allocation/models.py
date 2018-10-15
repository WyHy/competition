from django.db import models

# Create your models here.
from Profile.models import Profile
from TIFF.models import Image


class Allocation(models.Model):
    """
    任务分配信息
    """

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=u"名称")
    tiff = models.OneToOneField(Image, on_delete=models.CASCADE, verbose_name="大图")

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.user.username) + "-" + str(self.tiff.name)

    class Meta:
        verbose_name = u'任务分配信息'
        verbose_name_plural = u'任务分配信息'
