# Generated by Django 4.1.7 on 2023-05-18 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_post_require_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExceptionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exception_action', models.TextField(verbose_name='异常操作')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='时间戳')),
                ('user', models.ForeignKey(blank=True, db_column='username', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'verbose_name': 'log',
                'verbose_name_plural': 'logs',
                'db_table': 'exception_log',
            },
        ),
        migrations.CreateModel(
            name='FlavorPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor_title', models.TextField(verbose_name='倾向标题')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='时间戳')),
                ('user', models.ForeignKey(blank=True, db_column='username', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'verbose_name': 'log',
                'verbose_name_plural': 'logs',
                'db_table': 'flavor_post',
            },
        ),
        migrations.CreateModel(
            name='FlavorResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor_title', models.TextField(verbose_name='倾向标题')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='时间戳')),
                ('user', models.ForeignKey(blank=True, db_column='username', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'verbose_name': 'log',
                'verbose_name_plural': 'logs',
                'db_table': 'flavor_resource',
            },
        ),
        migrations.DeleteModel(
            name='Log',
        ),
    ]
