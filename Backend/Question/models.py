from django.db import models

# Create your models here.
from PathologyType.models import Type
from TIFF.models import Image


class Question(models.Model):
    """
    观众竞猜题目
    """

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    title = models.CharField(max_length=32, verbose_name=u"标题", null=True, blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="关联病理图像", unique=True)
    choices = models.ManyToManyField(Type, verbose_name="答案选项")
    remark = models.TextField(verbose_name="题目描述", null=True, blank=True)

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.image.name)

    class Meta:
        verbose_name = u'竞猜题目'
        verbose_name_plural = u'竞猜题目'
