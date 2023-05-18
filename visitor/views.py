import json
import random

from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tools.sms import YunTongXin
from user.models import User
import hashlib
# Create your views here.
# def visitor_views(request):
#     if request.method == 'GET':
#         pass
#     elif request.method == 'POST':
#         pass


    #def get(self,request):
     #   pass
#@CSRF
def register(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
      # nickname = json_obj['nickname']
    email = json_obj['email']
    password_1 = json_obj['password_1']
    password_2 = json_obj['password_2']
    telephone = json_obj['telephone']
    sms_num = json_obj['sms_num']
    if password_1 != password_2:
        result = {'code':10100,'error':'The password is not same'}
        return JsonResponse(result)

    old_code = cache.get('sms_%s' % (telephone))
    if not old_code:
        result = {'code': '10110', 'error': 'The code is wrong'}
        return JsonResponse(result)
    if int(sms_num) != old_code:
        result = {'code': '10111', 'error': 'The code is wrong'}
        return JsonResponse(result)

      # 用户名是否可用
    old_users = User.objects.filter(username=username)
    if old_users :
        result = {'code': 10101, 'error': 'The username is already existed'}
        return JsonResponse(result)
    p_m = hashlib.md5()
    p_m.update(password_1.encode())
    User.objects.create(username=username,nickname=username,password=p_m.hexdigest(),email=email,telephone=telephone)

      # 参数的基本检查：密码不能超过多少位，用户名是否可用
      # 异常返回：
      # result = {'code':10100,'error':'The username is already existed'}
      # return JsonResponse(result)
      # 异常码范围：10100 - 10199
    result = {'code': 200, 'username': username}
    return JsonResponse(result)
#pass
def sms_view(request):
    if request.method != 'POST':
        result = {'code':10108, 'error':'Please use POST'}
        return JsonResponse(result)
    json_str = request.body
    json_obj = json.loads(json_str)
    telephone = json_obj['telephone']
    # 生成随机码
    code = random.randint(1000, 9999)
    print('telephone', telephone, ' code', code)
    # 存储随机码 django-redis sudo pip3 install django-redis
    cache_key = 'sms_%s' % (telephone)
    # 检查是否已经有发过的且未过期的验证码
    old_code = cache.get(cache_key)
    if old_code:
        return JsonResponse({'code': 10111, 'error': 'The code is already existed'})

    cache.set(cache_key, code, 60)
    # 发送随机码 -> 短信
    send_sms(telephone, code)
    return JsonResponse({'code': 200})

def send_sms(telephone, code):

    config = {
        "accountSid": "2c94811c87fb7ec601882d4a7aa00f2e",
        "accountToken": "c96c2ecf30284a64b9a9a11f9f4bf797",
        "appId": "2c94811c87fb7ec601882d4a7be20f35",
        "templateId": "1"
    }
    yun = YunTongXin(**config)
    res = yun.run(telephone, code)
    return res