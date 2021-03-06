# Generated by Django 2.0.6 on 2018-11-07 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TIFF', '0004_image_case_no'),
        ('Label', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreenShot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='唯一主键')),
                ('x', models.FloatField(verbose_name='截图左上角坐标-x')),
                ('y', models.FloatField(verbose_name='截图左上角坐标-y')),
                ('w', models.FloatField(verbose_name='截图细胞宽度-w')),
                ('h', models.FloatField(verbose_name='截图细胞高度-h')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='处理时间')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TIFF.Image', verbose_name='关联病理图像')),
            ],
            options={
                'verbose_name': '截图信息',
                'verbose_name_plural': '截图信息',
            },
        ),
        migrations.AddField(
            model_name='cell',
            name='source_type',
            field=models.CharField(choices=[('AI', '智能标注'), ('MANUAL', '手工标注')], default='AI', max_length=16, verbose_name='标注类别'),
        ),
    ]
