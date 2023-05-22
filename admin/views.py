import hashlib
import json
import time

import jwt
from django.contrib.auth import user_logged_in
from django.shortcuts import render

from djangoProject import settings
from tools.user_dec import check_token, check_admin_token
# Create your views here.
from user.models import User, Post, Comment_for_post, FlavorPost, ExceptionUser, ExceptionPost, Resource, \
    FlavorResource, ExceptionResource, Admin_request
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
# 返回所有异常用户
@check_admin_token
def get_exception_users(request):
    if request.method == "GET":
        exception_users = ExceptionUser.objects.all()
        data = []
        for exception_user in exception_users:
            data.append({
                'user': exception_user.user.username,
                'reason': exception_user.exception_reason,
                'time': exception_user.timestamp,
            })
        return JsonResponse({'code': 200, 'data': data})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
#警告异常用户
@check_admin_token
def warn_exception_user(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        username = data['username']
        reason = data['reason']
        user=User.objects.get(username=username)
        user.is_waring=True
        user.save()
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
#删除异常用户
@check_admin_token
def delete_exception_user(request):
    if request.method == "POST":
        json_str = request.body.decode()
        data = json.loads(json_str)
        username = data['username']
        user=User.objects.get(username=username)
        user.delete()
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
#返回所有异常帖子
@check_admin_token
def get_exception_posts(request):
    if request.method == "GET":
        exception_posts = ExceptionPost.objects.all()
        data = []
        for exception_post in exception_posts:
            data.append({
                'post_id': exception_post.post_id,
                'post_title': Post.objects.get(id=exception_post.post_id).title,
                'reason': exception_post.exception_reason,
            })
        return JsonResponse({'code': 200, 'data': data})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})

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
            })
        return JsonResponse({'code': 200, 'data': data})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})

#返回所有申请成为管理员的用户
@check_admin_token
def get_admin_requests(request):
    if request.method == "GET":
        users=Admin_request.objects.all()
        data=[]
        for user in users:
            data.append({
                'username':user.username,
            })
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
#处理申请成为管理员的请求
@check_admin_token
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
        Admin_request.objects.filter(username=username).delete()
        return JsonResponse({'code': 200, 'data': 'success'})
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
