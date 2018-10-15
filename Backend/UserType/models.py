from django.db import models


# Create your models here.

class UserType(models.Model):
    """
    用户类型信息
    """

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    name = models.CharField(max_length=64, verbose_name=u"名称")
    description = models.CharField(max_length=1024, verbose_name=u"描述")

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.name)

    class Meta:
        verbose_name = u'用户类型'
        verbose_name_plural = u'用户类型'
