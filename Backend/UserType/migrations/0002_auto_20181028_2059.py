# Generated by Django 2.0.6 on 2018-10-28 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserType', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertype',
            name='description',
            field=models.CharField(max_length=128, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='usertype',
            name='name',
            field=models.CharField(max_length=32, verbose_name='名称'),
        ),
    ]