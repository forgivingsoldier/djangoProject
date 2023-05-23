import json
import time

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from tools.recommender import ContentBasedRecommender
from user.models import Post, User, Comment_for_post, FlavorPost, ExceptionPost, LikeNotice
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from tools.user_dec import check_token, get_username_by_request

# Create your views here.
@check_token
def post(request, authorName):
    author = request.myuser
    # 经验值增加
    author.experience += 5
    author.save()
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    title = json_obj['title']
    content = json_obj['content']
    require_level = json_obj['level']
    Post.objects.create(title=title, content=content, user=author, require_level=require_level, like_count=0,
                        comment_count=0, update_time=time.time(), )
    return JsonResponse({'code': 200})


@check_token
def delete(request, authorName):
    author = request.myuser
    if author.username != authorName:
        return JsonResponse({'code': 10205, 'error': '你没有权限删除别人的帖子,你的行为将被记录'})
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    title = json_obj['title']
    try:
        post = Post.objects.get(title=title, user=authorName)
    except Exception as e:
        return JsonResponse({'code': 10207, 'error': '帖子不存在'})
    post.delete()
    return JsonResponse({'code': 200})


# 获取指定作者的所有帖子(访问者有可能存在三种情况：访客、非作者的用户、作者；帖子无顺序)
def get_all_posts(request, authorName):
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
    posts = Post.objects.filter(user=authorName)
    res = {'code': 200, 'data': {}}
    posts_list = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        d['content'] = post.content
        d['like_count'] = post.like_count
        d['comment_count'] = post.comment_count
        d['update_time'] = post.update_time
        d['url']=reverse('get_post_by_id',kwargs={'post_id':post.id})
        posts_list.append(d)

    res['data']['nickname'] = author.nickname
    res['data']['posts'] = posts_list
    return JsonResponse(res)


# 按照时间顺序获取指定作者的所有帖子
def get_posts_by_time(request, authorName):
    try:
        author = User.objects.get(username=authorName)
    except Exception as e:
        return JsonResponse({'code': 10201, 'error': '用户不存在'})
    posts = Post.objects.filter(user=authorName).order_by('-update_time')
    res = {'code': 200, 'data': {}}
    posts_list = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        d['content'] = post.content
        d['like_count'] = post.like_count
        d['comment_count'] = post.comment_count
        d['update_time'] = post.update_time
        d['url']=reverse('get_post_by_id',kwargs={'post_id':post.id})
        posts_list.append(d)

    res['data']['posts'] = posts_list
    return JsonResponse(res)


# 按照点赞数获取指定作者的所有帖子
def get_posts_by_like(request, authorName):
    try:
        author = User.objects.get(username=authorName)
    except Exception as e:
        return JsonResponse({'code': 10201, 'error': '用户不存在'})
    posts = Post.objects.filter(user=authorName).order_by('-like_count')
    res = {'code': 200, 'data': {}}
    posts_list = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        d['content'] = post.content
        d['like_count'] = post.like_count
        d['comment_count'] = post.comment_count
        d['update_time'] = post.update_time
        d['url']=reverse('get_post_by_id',kwargs={'post_id':post.id})

        posts_list.append(d)

    res['data']['posts'] = posts_list
    return JsonResponse(res)


# 获取包含指定关键字的所有帖子
def get_posts_by_keyword(request, authorName):
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    keyword = json_obj['keyword']
    posts = Post.objects.filter(title__contains=keyword)
    res = {'code': 200, 'data': {}}
    posts_list = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        d['content'] = post.content
        d['like_count'] = post.like_count
        d['comment_count'] = post.comment_count
        d['update_time'] = post.update_time
        d['url']=reverse('get_post_by_id',kwargs={'post_id':post.id})

        posts_list.append(d)

    res['data']['posts'] = posts_list
    return JsonResponse(res)


# 按照评论数获取指定作者的所有帖子
def get_posts_by_comment(request, authorName):
    try:
        author = User.objects.get(username=authorName)
    except Exception as e:
        return JsonResponse({'code': 10201, 'error': '用户不存在'})
    posts = Post.objects.filter(user=authorName).order_by('-comment_count')
    res = {'code': 200, 'data': {}}
    posts_list = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        d['content'] = post.content
        d['like_count'] = post.like_count
        d['comment_count'] = post.comment_count
        d['update_time'] = post.update_time
        d['url']=reverse('get_post_by_id',kwargs={'post_id':post.id})
        posts_list.append(d)

    res['data']['posts'] = posts_list
    return JsonResponse(res)


# 按照点赞数获取所有帖子
def get_all_posts_by_like(request):
    posts = Post.objects.all().order_by('-like_count')
    res = {'code': 200, 'data': {}}
    posts_list = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        d['content'] = post.content
        d['like_count'] = post.like_count
        d['comment_count'] = post.comment_count
        d['update_time'] = post.update_time
        d['url']=reverse('get_post_by_id',kwargs={'post_id':post.id})
        posts_list.append(d)

    res['data']['posts'] = posts_list
    return JsonResponse(res)


# 按照评论数获取所有帖子
def get_all_posts_by_comment(request):
    posts = Post.objects.all().order_by('-comment_count')
    res = {'code': 200, 'data': {}}
    posts_list = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        d['content'] = post.content
        d['like_count'] = post.like_count
        d['comment_count'] = post.comment_count
        d['update_time'] = post.update_time
        d['url']=reverse('get_post_by_id',kwargs={'post_id':post.id})
        posts_list.append(d)

    res['data']['posts'] = posts_list
    return JsonResponse(res)


# 按照时间顺序获取所有帖子
def get_all_posts_by_time(request):
    posts = Post.objects.all().order_by('-update_time')
    res = {'code': 200, 'data': {}}
    posts_list = []
    for post in posts:
        d = {}
        d['id'] = post.id
        d['title'] = post.title
        d['content'] = post.content
        d['like_count'] = post.like_count
        d['comment_count'] = post.comment_count
        d['update_time'] = post.update_time
        d['url']=reverse('get_post_by_id',kwargs={'post_id':post.id})
        posts_list.append(d)

    res['data']['posts'] = posts_list
    return JsonResponse(res)


# 改动自己的帖子
@check_token
def put(request, authorName):
    user = request.myuser
    if user.username != authorName:
        return JsonResponse({'code': 10205, 'error': '无权限'})
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    title = json_obj['title']
    content = json_obj['content']
    try:
        post = Post.objects.get(title=title, user=authorName)
    except Exception as e:
        return JsonResponse({'code': 10207, 'error': '帖子不存在'})
    post.content = content
    post.update_time = time.time()
    post.save()
    return JsonResponse({'code': 200})


# 判断当前用户等级是否足够
def is_require_level(request, authorName):
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    title = json_obj['title']
    visitor_name = get_username_by_request(request)
    if visitor_name == authorName:
        return JsonResponse({'code': 200, 'data': {'allow': True}})
    if visitor_name == None:
        post_level = Post.objects.get(title=title, user=authorName).require_level
        if post_level == 1:
            return JsonResponse({'code': 200, 'data': {'allow': True}})
        else:
            return JsonResponse({'code': 200, 'data': {'allow': False}})
    if visitor_name != None:
        visitor = User.objects.get(username=visitor_name)
        post_level = Post.objects.get(title=title, user=authorName).require_level
        if visitor.level >= post_level:
            return JsonResponse({'code': 200, 'data': {'allow': True}})
        else:
            return JsonResponse({'code': 200, 'data': {'allow': False}})


# 给帖子点赞
@check_token
def like(request, authorName):
    user = request.myuser
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    title = json_obj['title']
    try:
        post = Post.objects.get(title=title, user=authorName)
    except Exception as e:
        return JsonResponse({'code': 10207, 'error': '帖子不存在'})
    # 浏览者经验值加1
    user.exp += 1
    user.save()
    # 记录在FlavorPost中
    FlavorPost.objects.create(user=user, post_id=post.id, title=post.title, timestamp=time.time())
    # 作者经验值加3
    author = User.objects.get(username=authorName)
    author.exp += 3
    post.like_count += 1
    post.save()
    # 创建 LikeNotice 记录
    LikeNotice.objects.create(
        user=author,
        which_like=1,  # 根据你的定义，1 代表帖子
        post=post,
        post_title=post.title,
        timestamp=time.time()
    )
    return JsonResponse({'code': 200})


# 给帖子取消点赞
@check_token
def unlike(request, authorName):
    user = request.myuser
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    title = json_obj['title']
    try:
        post = Post.objects.get(title=title, user=authorName)
    except Exception as e:
        return JsonResponse({'code': 10207, 'error': '帖子不存在'})
    post.like_count -= 1
    post.save()
    FlavorPost.objects.filter(user=user, post_id=post.id).delete()
    return JsonResponse({'code': 200})


# 获取指定id的帖子
def get_post_by_id(request, id):
    try:
        post = Post.objects.get(id=id)
    except Exception as e:
        return JsonResponse({'code': 10207, 'error': '帖子不存在'})
    res = {'code': 200, 'data': {}}
    d = {}
    d['id'] = post.id
    d['title'] = post.title
    d['content'] = post.content
    d['like_count'] = post.like_count
    d['comment_count'] = post.comment_count
    d['update_time'] = post.update_time
    res['data']['post'] = d
    # 浏览者经验值加1
    visitor_name = get_username_by_request(request)
    if visitor_name != None:
        visitor = User.objects.get(username=visitor_name)
        visitor.exp += 1
        visitor.save()
        # 记录在FlavorPost表中
        FlavorPost.objects.create(user=visitor, post_id=id, flavor_title=post.title, timestamp=time.time())
    # 作者经验值加3
    author = User.objects.get(username=post.user)
    author.exp += 3
    author.save()

    return JsonResponse(res)


# 举报帖子
@check_token
def report(self, request, authorName):
    user = request.myuser
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    id = json_obj['id']
    reson = json_obj['reson']
    try:
        post = Post.objects.get(id=id, user=authorName)
    except Exception as e:
        return JsonResponse({'code': 10207, 'error': '帖子不存在'})
    post.report_count += 1
    post.save()
    # 举报者经验值加1
    user.exp += 1
    user.save()
    # 记录在ExceptionPost表中
    ExceptionPost.objects.create(post_id=id, author=authorName, exception_reason=reson)
    return JsonResponse({'code': 200})


def recommend_post_for_user(request, userName):
    try:
        flavor_logs = FlavorPost.objects.filter(user=userName)
    except ObjectDoesNotExist:
        #进行随机推荐
        posts = Post.objects.all()
        posts_df = pd.DataFrame(posts.values('id', 'title'))
        recommender = ContentBasedRecommender(posts_df)
        recommended_post_ids = recommender.recommend_items([], 5)
        return JsonResponse({'recommended_posts': recommended_post_ids})

    # 获取用户浏览的所有内容的id
    post_ids = [log.post.id for log in flavor_logs]

    # 获取所有的内容和标题
    posts = Post.objects.all()
    posts_df = pd.DataFrame(posts.values('id', 'title'))

    # 创建推荐器
    recommender = ContentBasedRecommender(posts_df)

    # 获取推荐的内容id
    recommended_post_ids = recommender.recommend_items(post_ids, 5)
    recommended_posts = [
        {
            "id": post_id,
            "title": posts.get(id=post_id).title,
            "url": reverse('get_post_by_id', args=[post_id]),
        }
        for post_id in recommended_post_ids
    ]

    return JsonResponse({'recommended_posts': recommended_posts})
#获取关注者所有的帖子
@csrf_exempt
@check_token
def get_follow_post(request,username):
    if request.method == 'GET':
        user = request.myuser
        if user.username != username:
            result = {'code': 10205, 'error': '无权限'}
            return JsonResponse(result)
        follow_users = user.follow.all()
        post_list = []
        for follow_user in follow_users:
            posts = Post.objects.filter(user=follow_user)
            for post in posts:
                post_list.append(post)
        post_list.sort(key=lambda x: x.update_time, reverse=True)
        post_list = [{'id': post.id, 'title': post.title, 'url': reverse('get_post_by_id', args=[post.id])} for post in post_list]
        return JsonResponse({'code': 200, 'data': {'post_list': post_list}})
    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)
