# Generated by Django 4.1.7 on 2023-05-16 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_comment_user_alter_log_user_alter_post_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_time',
        ),
        migrations.AddField(
            model_name='post',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]