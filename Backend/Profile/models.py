from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from UserType.models import UserType


class Profile(models.Model):
    """
    用户信息
    """

    id = models.AutoField(primary_key=True, verbose_name='唯一主键')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    type = models.ForeignKey(UserType, on_delete=models.CASCADE, verbose_name=u"类型")

    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u"处理时间", auto_now=True)

    def __str__(self):
        return str(self.id) + "-" + str(self.user.first_name) + str(self.user.last_name) + "-" + str(self.type.name)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u'用户信息'
