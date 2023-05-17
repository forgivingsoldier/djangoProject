import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    phone = json_obj['phone']

    if password_1 != password_2:
        result = {'code':10100,'error':'The password is not same'}
        return JsonResponse(result)
      # 用户名是否可用
    old_users = User.objects.filter(username=username)
    if old_users :
        result = {'code': 10101, 'error': 'The username is already existed'}
        return JsonResponse(result)
    p_m = hashlib.md5()
    p_m.update(password_1.encode())
    User.objects.create(username=username,nickname=username,password=p_m.hexdigest(),email=email,telephone=phone)

      # 参数的基本检查：密码不能超过多少位，用户名是否可用
      # 异常返回：
      # result = {'code':10100,'error':'The username is already existed'}
      # return JsonResponse(result)
      # 异常码范围：10100 - 10199
    result = {'code': 200, 'username': username}
    return JsonResponse(result)
#pass