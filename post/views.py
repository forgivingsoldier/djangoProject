import json
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user.models import Post, User
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from tools.user_dec import check_token, get_username_by_request

# Create your views here.
class postViews(View):


    @method_decorator(check_token)
    def post(self, request, authorName):

        author=request.myuser
        json_str = request.body.decode()
        json_obj = json.loads(json_str)
        title = json_obj['title']
        content = json_obj['content']
        require_level = json_obj['level']
        Post.objects.create(title=title, content=content, user=author, require_level=require_level, like_count=0, comment_count=0,update_time=time.time(),)
        return JsonResponse({'code':200})

    @method_decorator(check_token)
    def delete(self,request,authorName):
        author=request.myuser
        json_str = request.body.decode()
        json_obj = json.loads(json_str)
        title = json_obj['title']
        try:
            post = Post.objects.get(title=title, user=author)
        except Exception as e:
            return JsonResponse({'code': 10205, 'error': '帖子不存在'})
        post.delete()
        return JsonResponse({'code': 200})


    #获取指定作者的所有帖子(访问者有可能存在三种情况：访客、非作者的用户、作者)
    def get_all_posts(self,request,authorName):

        try:
            author = User.objects.get(username=authorName)
        except Exception as e:
            return JsonResponse({'code': 10201, 'error': '用户不存在'})
        """""
        visitorName = get_username_by_request(request)
        if visitorName == authorName:
            is_requere_level = 1
        else:
            is_requere_level = 0
        """""
        posts = Post.objects.filter(user=author)
        res = {'code':200, 'data': {}}
        posts_list = []
        for post in posts:
            d={}
            d['title'] = post.title
            d['content'] = post.content
            d['like_count'] = post.like_count
            d['comment_count'] = post.comment_count
            d['update_time'] = post.update_time

            posts_list.append(d)


        res['data']['nickname'] = author.nickname
        res['data']['posts'] = posts_list
        return JsonResponse(res)
    #获取包含指定关键字的所有帖子
    #def get_posts_by_keyword(self,request,authorName):






    pass