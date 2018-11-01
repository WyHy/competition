from django.db import models


# Create your models here.

class Image(models.Model):
    """
    病理图像 原图信息
    """
    STATUS_CHOICES = (
        ("CREATED", "待处理"),
        ("SUCCESS", "处理完成"),
        ("FAIL", "处理失败"),
        ("DELETED", "已删除"),
    )

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    name = models.CharField(max_length=64, verbose_name=u"图像名称")
    case_no = models.CharField(max_length=64, verbose_name=u"病理号", default='-')
    path = models.CharField(max_length=512, verbose_name=u"图像路径")
    progress = models.CharField(max_length=16, verbose_name=u"当前算法处理进度", default='-')
    result_auto = models.CharField(max_length=32, verbose_name=u"算法诊断结果", default='-')
    result_manual = models.CharField(max_length=32, verbose_name=u"医生诊断结果", default='-')
    result_status = models.CharField(max_length=32, verbose_name=u"标准诊断结果", default='-')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="CREATED", verbose_name=u"状态")
    remark = models.TextField(verbose_name=u"故障原因", blank=True, null=True)

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.name)

    class Meta:
        verbose_name = u'病理图像原图'
        verbose_name_plural = u'病理图像原图'
