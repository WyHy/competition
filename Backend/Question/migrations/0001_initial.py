# Generated by Django 2.0.6 on 2018-11-15 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('PathologyType', '0003_auto_20181030_1649'),
        ('TIFF', '0006_auto_20181115_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='唯一主键')),
                ('title', models.CharField(blank=True, max_length=32, null=True, verbose_name='细胞类别')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='题目描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='处理时间')),
                ('choices', models.ManyToManyField(to='PathologyType.Type', verbose_name='答案选项')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TIFF.Image', verbose_name='关联病理图像')),
            ],
            options={
                'verbose_name': '竞猜题目',
                'verbose_name_plural': '竞猜题目',
            },
        ),
    ]
