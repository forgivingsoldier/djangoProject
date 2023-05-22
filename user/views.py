import hashlib
import time
from random import random

from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse

from tools.sms import YunTongXin
# Create your views here.
from django.contrib.auth import authenticate, user_logged_in, user_logged_out
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import jwt
from django.conf import settings

from tools.user_dec import check_token
from user.models import User, Admin_request, Post, LikeNotice, CommentNotice
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
            user = User.objects.get(username=username)
        except Exception as e:
            result = {'code': 10201, 'error': '用户不存在'}
            return JsonResponse(result)


        p_m = hashlib.md5();
        p_m.update(password.encode());
        if(user.password != p_m.hexdigest()):
            result = {'code': 10202, 'error': '输入密码错误'}
            return JsonResponse(result)
        user.experience += 2
        is_warning=user.is_waring
        user.save()
        # 用户验证成功，生成JWT令牌
        key=settings.JWT_TOKEN_KEY
        now_time = time.time()
        payload = {'username': username, 'role':user.role}
        token = jwt.encode(payload, key, algorithm='HS256')
        result = {'code': 200, 'username': username, 'data': {'token': token,'is_warning':is_warning}}
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
        #关注者数量
        follow_num = user.follow.all().count()
        result = {'code': 200, 'username': username, 'data': {'nickname': user.nickname, 'email': user.email,
                                                               'role': user.role, 'experience': user.experience,
                                                               'level': user.level,'follow_number':follow_num,'avatar': str(user.avatar), 'signature': user.signature}}
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
def change_password_by_phone(request,username):
    if request.method == 'POST':
        json_str = request.body.decode()
        data = json.loads(json_str)
        telephone = data['telephone']
        sms_num = data['sms_num']
        user = request.myuser

        old_code = cache.get('sms_%s' % (telephone))
        if not old_code:
            result = {'code': '10203', 'error': '验证码错误'}
            return JsonResponse(result)
        if int(sms_num) != old_code:
            result = {'code': '10203', 'error': '验证码错误'}
            return JsonResponse(result)

        p_m = hashlib.md5();
        p_m.update(data['password'].encode());
        user.password = p_m.hexdigest()

        user.save()
        return JsonResponse({'code': 200})

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)


def sms_view(request):
    if request.method != 'POST':
        result = {'code':10200, 'error':'请求方式错误'}
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
        return JsonResponse({'code': 10204, 'error': '验证码已发送'})

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
            result = {'code': 10205, 'error': '无权限的操作'}
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
            result = {'code': 10205, 'error': '无权限'}
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
#申请成为管理员
@csrf_exempt
@check_token
def apply_admin(request,username):
    if request.method == 'POST':
        user = request.myuser
        if user.username != username:
            result = {'code': 10205, 'error': '无权限'}
            return JsonResponse(result)
        Admin_request.objects.create(user=user,timestamp=time.time())
        user.save()
        return JsonResponse({'code': 200})
    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)

#关注
@csrf_exempt
@check_token
def follow(request,username):
    if request.method == 'POST':
        user = request.myuser
        if user.username != username:
            result = {'code': 10205, 'error': '无权限'}
            return JsonResponse(result)
        json_str = request.body.decode()
        data = json.loads(json_str)
        follow_user_name = data['follow_user_name']
        follow_user = User.objects.filter(username=follow_user_name).first()
        if not follow_user:
            result = {'code': 10208, 'error': '关注的用户不存在'}
            return JsonResponse(result)
        if user == follow_user:
            result = {'code': 10209, 'error': '不能关注自己'}
            return JsonResponse(result)
        if user.follow.filter(username=follow_user_name).exists():
            result = {'code': 10210, 'error': '已关注'}
            return JsonResponse(result)
        user.follow.add(follow_user)
        user.save()
        return JsonResponse({'code': 200})
    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)


#取消关注
@csrf_exempt
@check_token
def unfollow(request,username):
    if request.method == 'POST':
        user = request.myuser
        if user.username != username:
            result = {'code': 10205, 'error': '无权限'}
            return JsonResponse(result)
        json_str = request.body.decode()
        data = json.loads(json_str)
        follow_user_name = data['follow_user_name']
        follow_user = User.objects.filter(username=follow_user_name).first()
        if not follow_user:
            result = {'code': 10206, 'error': '关注的用户不存在'}
            return JsonResponse(result)
        if user == follow_user:
            result = {'code': 10207, 'error': '不能关注自己'}
            return JsonResponse(result)
        if not user.follow.filter(username=follow_user_name).exists():
            result = {'code': 10209, 'error': '未关注'}
            return JsonResponse(result)
        user.follow.remove(follow_user)
        user.save()
        return JsonResponse({'code': 200})
    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)

def get_follow_likes(request):
    user = request.myuser
    # 获取用户的所有未读点赞通知
    unread_likes = LikeNotice.objects.filter(user=user).order_by('-timestamp')
    # 将结果转换为字典列表，以便能够将其序列化为JSON
    unread_likes_list = [{
        'id': like.id,
        'which_like': like.which_like,
        'post_id': like.post.id if like.post else None,
        'post_title': like.post_title,
        'resource_id': like.resource.id if like.resource else None,
        'resource_title': like.resource_title,
        'comment_id': like.comment.id if like.comment else None,
        'timestamp': like.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'is_read': like.is_read,
        'post_url':reverse('get_post_by_id',args=(like.post.id,)) if like.post else None,
       # 'resource_url':reverse('get_resource_by_id',args=(like.resource.id,)) if like.resource else None,
        'comment_url':reverse('get_comment_by_id',args=(like.comment.id,)) if like.comment else None,
    } for like in unread_likes]
    unread_likes.update(is_read=True)
    # 返回结果
    return JsonResponse({'code': 200, 'unread_likes': unread_likes_list})

def get_follow_comments(request):
    user = request.myuser
    # 获取用户的所有未读评论通知
    unread_comments = CommentNotice.objects.filter(user=user).order_by('-timestamp')
    # 将结果转换为字典列表，以便能够将其序列化为JSON
    unread_comments_list = [{
        'id': comment.id,
        'which_comment': comment.which_comment,
        'post_id': comment.post.id if comment.post else None,
        'post_title': comment.post_title,
        'resource_id': comment.resource.id if comment.resource else None,
        'resource_title': comment.resource_title,
        'comment_id': comment.comment.id if comment.comment else None,
        'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'is_read': comment.is_read,
        'post_url':reverse('get_post_by_id',args=(comment.post.id,)) if comment.post else None,
        #'resource_url':reverse('get_resource_by_id',args=(comment.resource.id,)) if comment.resource else None,
        'comment_url':reverse('get_comment_by_id',args=(comment.comment.id,)) if comment.comment else None,
    } for comment in unread_comments]
    unread_comments.update(is_read=True)
    # 返回结果
    return JsonResponse({'code': 200, 'unread_comments': unread_comments_list})