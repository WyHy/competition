# Generated by Django 2.1.2 on 2018-10-15 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='唯一主键')),
                ('name', models.CharField(max_length=64, verbose_name='图像名称')),
                ('path', models.CharField(max_length=512, verbose_name='图像路径')),
                ('progress', models.CharField(max_length=16, verbose_name='当前算法处理进度')),
                ('result_auto', models.CharField(max_length=32, verbose_name='算法诊断结果')),
                ('result_manual', models.CharField(max_length=32, verbose_name='医生诊断结果')),
                ('result_status', models.CharField(max_length=32, verbose_name='标准诊断结果')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='处理时间')),
            ],
            options={
                'verbose_name_plural': '病理图像原图',
                'verbose_name': '病理图像原图',
            },
        ),
    ]
