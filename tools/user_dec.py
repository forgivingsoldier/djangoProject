import jwt
from django.conf import settings
from django.http import JsonResponse
from django.templatetags.static import static

from user.models import User

online_user_num = 0
def check_token(func):
    def wrapper(request, *args, **kwargs):
        # 获取token
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': 10206, 'error': '请登录'}
            return JsonResponse(result)
        # 验证token
        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms='HS256')
        except Exception as e:
            result = {'code': 10206, 'error': '请登录'}
            return JsonResponse(result)

        username = res['username']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            result = {'code': 10205, 'error': '用户已被管理员删除或你在试图修改别人的信息'}
            return JsonResponse(result)
        request.myuser = user
        return func(request, *args, **kwargs)
    return wrapper



def get_username_by_request(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms='HS256')
    except Exception as e:
        return None
    username = res['username']
    return username