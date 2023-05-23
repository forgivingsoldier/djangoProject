# Generated by Django 4.1.7 on 2023-05-21 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_admin_requst_admin_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('content', models.TextField(verbose_name='通知内容')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='时间戳')),
                ('user', models.ForeignKey(blank=True, db_column='username', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'user_notice',
            },
        ),
    ]