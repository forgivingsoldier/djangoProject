# Generated by Django 4.1.7 on 2023-05-26 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_exceptioncomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='exceptioncomment',
            name='exception_reason',
            field=models.TextField(default='无', verbose_name='异常原因'),
        ),
    ]
