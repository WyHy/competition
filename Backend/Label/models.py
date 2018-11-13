from django.db import models

# Create your models here.
from PathologyType.models import Type
from TIFF.models import Image


class Cell(models.Model):
    """
    算法自动识别 / 手工标记 的细胞信息
    """

    SOURCE_TYPE_CHOICES = (
        ("AI", "智能标注"),
        ("MANUAL", "手工标注"),
    )

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="关联病理图像")
    x = models.FloatField(verbose_name='标注点左上角坐标-x')
    y = models.FloatField(verbose_name='标注点左上角坐标-y')
    w = models.FloatField(verbose_name='标注点细胞宽度-w')
    h = models.FloatField(verbose_name='标注点细胞高度-h')
    cell_type = models.CharField(max_length=32, verbose_name=u"细胞类别")
    accuracy = models.FloatField(verbose_name='相似度', blank=True, null=True)
    source_type = models.CharField(max_length=16, choices=SOURCE_TYPE_CHOICES, default="AI", verbose_name=u"标注类别")

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.image.name)

    class Meta:
        verbose_name = u'标注信息'
        verbose_name_plural = u'标注信息'


class ScreenShot(models.Model):
    """
    截图信息
    """

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="关联病理图像")
    x = models.FloatField(verbose_name='截图左上角坐标-x')
    y = models.FloatField(verbose_name='截图左上角坐标-y')
    w = models.FloatField(verbose_name='截图细胞宽度-w')
    h = models.FloatField(verbose_name='截图细胞高度-h')

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.name)

    class Meta:
        verbose_name = u'截图信息'
        verbose_name_plural = u'截图信息'
