import hashlib
import json
import time

import jwt
from django.contrib.auth import user_logged_in
from django.shortcuts import render
from django.urls import reverse

from djangoProject import settings
from tools.user_dec import check_token, check_admin_token
# Create your views here.
from user.models import User, Post, Comment_for_post, FlavorPost, ExceptionUser, ExceptionPost, Resource, \
    FlavorResource, ExceptionResource, Admin_request, ExceptionComment,UserWarningNotice
from django.http import JsonResponse



#管理员登录
def admin_login(request):
    if request.method == 'POST':
        json_str = request.body.decode()
        # print(json_str)
        data = json.loads(json_str)
        username = data['username']
        password = data['password']

        try:
            user = User.objects.get(username=username);
        except Exception as e:
            result = {'code': 10201, 'error': '用户不存在'}
            return JsonResponse(result)
        user.experience+=2
        user.save()

        p_m = hashlib.md5();
        p_m.update(password.encode());
        if user.password != p_m.hexdigest()or(user.role != "admin"):
            result = {'code': 10202, 'error': '输入密码错误'}
            return JsonResponse(result)

        # 用户验证成功，生成JWT令牌
        key=settings.JWT_TOKEN_KEY
        now_time = time.time()
        payload = {'username': username, 'role':user.role}
        token = jwt.encode(payload, key, algorithm='HS256')
        result = {'code': 200, 'username': username, 'data': {'token': token}}
        return JsonResponse(result)

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)



#返回所有异常用户
#@check_admin_token
def get_exception_users(request):
    if request.method == "GET":
        exception_users = ExceptionUser.objects.all()
        data = []
        for exception_user in exception_users:
            data.append({
                'user': exception_user.user.username,
                'reason': exception_user.exception_action,
                'time': exception_user.timestamp,
            })
        return JsonResponse({'code': 200, 'data': data})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
#警告异常用户
#@check_admin_token
def warn_exception_user(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        username = data['username']
        reason = data['reason']
        user=User.objects.get(username=username)
        user.is_waring=True
        user.save()
        UserWarningNotice.objects.create(user=user,is_read=False,content=reason,timestamp=time.time())
        ExceptionUser.objects.filter(user=user).delete()
        return JsonResponse({'code': 200, 'data': '警告成功'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
#删除异常用户
#@check_admin_token
def delete_exception_user(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        username = data['username']
        user=User.objects.get(username=username)
        user.delete()
        ExceptionUser.objects.filter(user=user).delete()
        return JsonResponse({'code': 200, 'data': '删除成功'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
#返回所有异常帖子
#@check_admin_token
def get_exception_posts(request):
    if request.method == "GET":
        exception_posts = ExceptionPost.objects.all()
        data = []
        for exception_post in exception_posts:
            data.append({
                'id': exception_post.post_id.id,
                'title': Post.objects.get(id=exception_post.post_id.id).title,
                'reason': exception_post.exception_reason,
                'url':reverse('get_post_by_id',kwargs={'id':exception_post.post_id.id})
            })
        return JsonResponse({'code': 200, 'data': data})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
'''''
#返回所有异常资源
@check_admin_token
def get_exception_resources(request):
    if request.method == "GET":
        exception_resources = ExceptionResource.objects.all()
        data = []
        for exception_resource in exception_resources:
            data.append({
                'resource_id': exception_resource.resource_id,
                'resource_name': Resource.objects.get(id=exception_resource.resource_id).name,
                'reason': exception_resource.exception_reason,
                'url':reverse('get_resource_by_id',kwargs={'id':exception_resource.resource_id})
            })
        return JsonResponse({'code': 200, 'data': data})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
'''''
#返回所有异常评论
#@check_admin_token
def get_exception_comments(request):
    if request.method == "GET":
        exception_comments = ExceptionComment.objects.all()
        data = []
        for exception_comment in exception_comments:
            data.append({
                'id': exception_comment.comment_id.id,
                'content': Comment_for_post.objects.get(id=exception_comment.comment_id.id).content,
                'reason': exception_comment.exception_reason,
                'url':reverse('get_comment_by_id',kwargs={'comment_id':exception_comment.comment_id.id})
            })
        return JsonResponse({'code': 200, 'data': data})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
#返回所有申请成为管理员的用户
#@check_admin_token
def get_admin_requests(request):
    if request.method == "GET":
        users=Admin_request.objects.all()
        data=[]
        for user in users:
            data.append({
                'username':user.user.username
            })
        return JsonResponse({'code': 200, 'data': data})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
#处理申请成为管理员的请求
#@check_admin_token
def handle_admin_request(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        username = data['username']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return JsonResponse({'code': 10201, 'error': '用户不存在'})
        user.role="admin"
        user.save()
        Admin_request.objects.filter(user=username).delete()
        return JsonResponse({'code': 200, 'data': 'success'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})

#拒绝申请成为管理员的请求
#@check_admin_token
def refuse_admin_request(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        username = data['username']
        Admin_request.objects.filter(user=username).delete()
        return JsonResponse({'code': 200, 'data': 'success'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})

#@check_admin_token
def delete_post(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        post_id = data['id']
        Post.objects.filter(id=post_id).delete()
        return JsonResponse({'code': 200, 'data': 'success'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})

#忽略异常帖子
#@check_admin_token
def ignore_exception_post(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        post_id = data['id']
        ExceptionPost.objects.filter(post_id=post_id).delete()
        return JsonResponse({'code': 200, 'data': 'success'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})

#删除资源
#@check_admin_token
def delete_resource(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        resource_id = data['id']
        Resource.objects.filter(id=resource_id).delete()
        return JsonResponse({'code': 200, 'data': 'success'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
#

#删除异常资源
#@check_admin_token
def ignore_exception_resource(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        resource_id = data['resource_id']
        ExceptionResource.objects.filter(resource_id=resource_id).delete()
        return JsonResponse({'code': 200, 'data': 'success'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})

#忽略异常评论
#@check_admin_token
def ignore_exception_comment(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        comment_id = data['id']
        ExceptionComment.objects.filter(comment_id=comment_id).delete()
        return JsonResponse({'code': 200, 'data': 'success'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
def delete_comment(request):
    json_str = request.body.decode()
    data = json.loads(json_str)
    comment_id = data['id']
    comment = Comment_for_post.objects.get(id=comment_id)
    if request.method == "DELETE":
            # 递归删除所有附属于这个评论的评论
            def delete_recursive(comment):
                # 获取此评论的所有回复
                replies = Comment_for_post.objects.filter(parent_comment=comment)
                for reply in replies:
                    delete_recursive(reply)
                    post = comment.post_id
                    post.comment_count -= 1
                    post.save()

                # 当所有回复都已删除，可以安全删除此评论
                comment.delete()

            delete_recursive(comment)

            # 更新文章的评论数

            return JsonResponse({'code': 200, 'message': '删除成功'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})

#忽略异常用户
#@check_admin_token
def ignore_exception_user(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        username = data['username']
        ExceptionUser.objects.filter(user=username).delete()
        return JsonResponse({'code': 200})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})