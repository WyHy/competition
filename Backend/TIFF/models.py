from django.db import models


# Create your models here.

class Image(models.Model):
    """
    病理图像 原图信息
    """

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    name = models.CharField(max_length=64, verbose_name=u"图像名称")
    path = models.CharField(max_length=512, verbose_name=u"图像路径")
    progress = models.CharField(max_length=16, verbose_name=u"当前算法处理进度", default='-')
    result_auto = models.CharField(max_length=32, verbose_name=u"算法诊断结果", default='-')
    result_manual = models.CharField(max_length=32, verbose_name=u"医生诊断结果", default='-')
    result_status = models.CharField(max_length=32, verbose_name=u"标准诊断结果", default='-')

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.name)

    class Meta:
        verbose_name = u'病理图像原图'
        verbose_name_plural = u'病理图像原图'
