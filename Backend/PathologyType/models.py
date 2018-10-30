from django.db import models


# Create your models here.

class Type(models.Model):
    """
    病理类型信息
    """

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    name = models.CharField(max_length=32, verbose_name=u"名称", unique=True)
    color = models.CharField(max_length=16, verbose_name=u"显示颜色")
    description = models.CharField(max_length=128, verbose_name=u"描述")

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.name)

    class Meta:
        verbose_name = u'病理类型'
        verbose_name_plural = u'病理类型'
