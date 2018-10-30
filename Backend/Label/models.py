from django.db import models


# Create your models here.
from PathologyType.models import Type
from TIFF.models import Image


class Cell(models.Model):
    """
    算法自动识别的细胞信息
    """

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="关联病理图像")
    x = models.FloatField(verbose_name='标注点左上角坐标-x')
    y = models.FloatField(verbose_name='标注点左上角坐标-y')
    w = models.FloatField(verbose_name='标注点细胞宽度-w')
    h = models.FloatField(verbose_name='标注点细胞高度-h')
    cell_type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="细胞类别")

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.name)

    class Meta:
        verbose_name = u'标注信息'
        verbose_name_plural = u'标注信息'
