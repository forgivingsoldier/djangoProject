import json
import time
from datetime import datetime

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

from tools.user_dec import check_token, get_username_by_request
from user.models import Post, Comment_for_post, User, FlavorPost


@check_token
def create_comment_for_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        json_str = request.body.decode()
        data = json.loads(json_str)
        content = data.get('content')

        comment = Comment_for_post.objects.create(
            content=content,
            user=request.myuser,
            post_id=post,
            comment_time=datetime.fromtimestamp(time.time()),
        )
        request.myuser.experience += 1
        request.myuser.save()

        post.comment_count += 1
        post.save()

        return JsonResponse(get_comment_data(comment))
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=400)

@check_token
def create_comment_for_comment(request, comment_id):
    if request.method == "POST":
        parent_comment = Comment_for_post.objects.get(id=comment_id)
        data = json.loads(request.body)
        content = data.get('content')

        if not content:
            return JsonResponse({"error": "需要提供评论内容"}, status=400)
        user = request.myuser
        comment = Comment_for_post.objects.create(
            content=content,
            user=user,
            post_id=parent_comment.post_id,
            parent_comment=parent_comment,
            comment_time=datetime.fromtimestamp(time.time()),
        )
        user.experience += 1
        user.save()
        comment.post_id.comment_count += 1
        comment.post_id.save()

        return JsonResponse('code:200')
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=400)
def get_comment_data(comment):
    replies = [get_comment_data(reply) for reply in comment.replies.all()]
    return {
        'content': comment.content,
        'created_at': comment.comment_time.isoformat(),
        'author': comment.user.username,
        'replies': replies
    }

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = [get_comment_data(comment) for comment in post.comments.filter(parent_comment=None)]
    data = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'updated_at': post.update_time.isoformat(),
        'author': post.user.username,
        'comments': comments
    }
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
    return JsonResponse(data)
