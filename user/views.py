import hashlib
import time

from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import jwt
from django.conf import settings

from tools.user_dec import check_token
from user.models import User;
from django.conf import settings


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

        p_m = hashlib.md5();
        p_m.update(password.encode());
        if(user.password != p_m.hexdigest()):
            result = {'code': 10202, 'error': '输入密码错误'}
            return JsonResponse(result)

        # 用户验证成功，生成JWT令牌
        key=settings.JWT_TOKEN_KEY
        now_time = time.time()
        payload = {'username': username, 'exp': int(now_time + 60 * 60 * 24)}
        token = jwt.encode(payload, key, algorithm='HS256')
        result = {'code': 200, 'username': username, 'data': {'token': token}}
        return JsonResponse(result)

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)

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
