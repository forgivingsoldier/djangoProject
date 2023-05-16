from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(models.Model):
    ROLE_CHOICES = [
        ('visitor', '访客'),
        ('user', '用户'),
        ('admin', '管理员'),
    ]
    id = models.IntegerField(blank=True, null=True)
    username = models.CharField('用户名', max_length=255, unique=True, db_index=True, primary_key=True, blank=False)
    password = models.CharField('密码', max_length=255, blank=False,default='123456')
    email = models.EmailField('邮箱', blank=True)
    nickname = models.CharField('昵称', max_length=255, blank=True)
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='visitor')
    experience = models.IntegerField('经验值', default=0)
    level = models.IntegerField('等级', default=1)
    register_time = models.DateTimeField('注册时间', auto_now_add=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)  # 新增头像字段
    signature = models.CharField('个性签名', max_length=255, blank=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('subject', '学科'),
        ('type', '资源类型'),
    ]
    name = models.CharField('资源名称', max_length=255)
    author = models.CharField('作者', max_length=255)
    description = models.TextField('资源描述')
    category = models.CharField('资源分类', max_length=20, choices=CATEGORY_CHOICES)
    file = models.FileField('文件', upload_to='resources/')  # 新增文件字段
    file_url = models.URLField('文件链接')
    download_count = models.IntegerField('下载次数', default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    upload_time = models.DateTimeField('上传时间', default=timezone.now)

    class Meta:
        verbose_name = 'resource'
        verbose_name_plural = 'resources'


class Post(models.Model):
    title = models.CharField('帖子标题', max_length=255)
    content = models.TextField('帖子内容')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    post_time = models.DateTimeField('发布时间', default=timezone.now)
    like_count = models.IntegerField('点赞次数', default=0)
    comment_count = models.IntegerField('评论次数', default=0)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

class Comment(models.Model):
    content = models.TextField('评论内容')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment_time = models.DateTimeField('评论时间', default=timezone.now)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

class Log(models.Model):
    ACTION_CHOICES = [
        ('login', '登录'),
        ('post', '发帖'),
        ('comment', '评论'),
        ('like', '点赞'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    action = models.CharField('动作', max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField('时间戳', auto_now_add=True)

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'
