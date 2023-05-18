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
    telephone = models.CharField('手机号', max_length=11, blank=True,default='12345678910')

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Resource(models.Model):

    name = models.CharField('资源名称', max_length=255)
    author = models.CharField('作者', max_length=255)
    description = models.TextField('资源描述')
    filetype = models.CharField('资源文件分类', max_length=255,default ='其他' )
    subject = models.CharField('资源学科', max_length=255,default ='其他' )
    file = models.FileField('文件', upload_to='resources/')  # 新增文件字段
    file_url = models.URLField('文件链接')
    download_count = models.IntegerField('下载次数', default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,db_column='username')
    upload_time = models.DateTimeField('上传时间', default=timezone.now)

    class Meta:
        db_table = 'resource'
        verbose_name = 'resource'
        verbose_name_plural = 'resources'


class Post(models.Model):
    title = models.CharField('帖子标题', max_length=255)
    content = models.TextField('帖子内容')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,db_column='username')
    update_time = models.DateTimeField('更新时间', auto_now=True)
    like_count = models.IntegerField('点赞次数', default=0)
    comment_count = models.IntegerField('评论次数', default=0)
    require_level = models.IntegerField('要求等级', default=1)

    class Meta:
        db_table = 'post'
        verbose_name = 'post'
        verbose_name_plural = 'posts'
2
class Comment(models.Model):
    content = models.TextField('评论内容')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,db_column='username')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment_time = models.DateTimeField('评论时间', default=timezone.now)

    class Meta:
        db_table = 'comment'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

class ExceptionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,db_column='username')
    exception_action = models.TextField("异常操作")
    timestamp = models.DateTimeField('时间戳', auto_now_add=True)

    class Meta:
        db_table = 'exception_log'
        verbose_name = 'log'
        verbose_name_plural = 'logs'
class FlavorPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,db_column='username')
    flavor_title= models.TextField("倾向标题")
    timestamp = models.DateTimeField('时间戳', auto_now_add=True)

    class Meta:
        db_table = 'flavor_post'
        verbose_name = 'log'
        verbose_name_plural = 'logs'
class FlavorResource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,db_column='username')
    flavor_title= models.TextField("倾向标题")
    timestamp = models.DateTimeField('时间戳', auto_now_add=True)

    class Meta:
        db_table = 'flavor_resource'
        verbose_name = 'log'
        verbose_name_plural = 'logs'