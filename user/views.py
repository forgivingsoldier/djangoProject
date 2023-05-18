import hashlib
import time

from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, user_logged_in, user_logged_out
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import jwt
from django.conf import settings

from tools.user_dec import check_token
from user.models import User
from django.conf import settings
#登录
@csrf_exempt
def login(request):
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
        '''''
        p_m = hashlib.md5();
        p_m.update(password.encode());
        if(user.password != p_m.hexdigest()):
            result = {'code': 10202, 'error': '输入密码错误'}
            return JsonResponse(result)
        '''''
        # 用户验证成功，生成JWT令牌
        key=settings.JWT_TOKEN_KEY
        now_time = time.time()
        payload = {'username': username, 'exp': int(now_time + 60 * 60 * 24)}
        token = jwt.encode(payload, key, algorithm='HS256')
        result = {'code': 200, 'username': username, 'data': {'token': token}}
        user_logged_in.send(sender=None, user=user, request=request)
        return JsonResponse(result)

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)

#获取用户信息
def info(request, username):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            result = {'code': 10201, 'error': '用户不存在'}
            return JsonResponse(result)

        result = {'code': 200, 'username': username, 'data': {'nickname': user.nickname, 'email': user.email,
                                                               'role': user.role, 'experience': user.experience,
                                                               'level': user.level,'avatar': str(user.avatar), 'signature': user.signature}}
        return JsonResponse(result)

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)

#修改用户信息
@csrf_exempt
@check_token
def change_info(request,username):
    if request.method == 'PUT':
        json_str = request.body.decode()
        data = json.loads(json_str)

        user = request.myuser

        user.nickname = data['nickname']
        user.email = data['email']
        user.signature = data['signature']


        user.save()
        return JsonResponse({'code': 200})

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)

#修改用户头像
@csrf_exempt
@check_token
def change_avatar(request,username):
    if request.method == 'POST':
        user = request.myuser
        user.avatar = request.FILES['avatar']
        user.save()
        return JsonResponse({'code': 200})

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)

#修改密码
@csrf_exempt
@check_token
def change_password(request,username):
    if request.method == 'PUT':
        json_str = request.body.decode()
        data = json.loads(json_str)

        user = request.myuser

        p_m = hashlib.md5();
        p_m.update(data['old_password'].encode());
        if(user.password != p_m.hexdigest()):
            result = {'code': 10202, 'error': '输入密码错误'}
            return JsonResponse(result)

        p_m = hashlib.md5();
        p_m.update(data['new_password'].encode());
        user.password = p_m.hexdigest()

        user.save()
        return JsonResponse({'code': 200})

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)

# 忘记密码后通过验证发送给手机的验证码修改密码
# @csrf_exempt
# def change_password_by_phone(request,username):

# 退出登录
@csrf_exempt
@check_token
def logout(request,username):
    if request.method == 'POST':
        result = {'code': 200}
        user_logged_out.send(sender=None, user=request.myuser, request=request)
        return JsonResponse(result)
    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)
# 注销账号
@csrf_exempt
@check_token
def delete_account(request,username):
    if request.method == 'DELETE':
        user = request.myuser
        if user.username != username:
            result = {'code': 10208, 'error': '无权限'}
            return JsonResponse(result)
        user.delete()
        return JsonResponse({'code': 200})

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)

#根据经验值判断用户是否升级
@csrf_exempt
@check_token
def check_level(request,username):
    if request.method == 'GET':
        user = request.myuser
        if user.username != username:
            result = {'code': 10208, 'error': '无权限'}
            return JsonResponse(result)
        if user.experience>=5:
            user.level+=1
            user.experience-=5
            user.save()

        return JsonResponse({'code': 200,'data':{'level':user.level,'experience':user.experience}})
    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)

#获取在线用户数
def get_online_user_num(request):
    if request.method == 'GET':
        online_users = cache.get('online_users', [])
        # online_user_num = len(online_users)
        result = {'code': 200, 'data': {'online_user_num': online_users}}
        return JsonResponse(result)
    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)