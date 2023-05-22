import json
import time
from datetime import datetime

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

from tools.user_dec import check_token, get_username_by_request
from user.models import Post, Comment_for_post, User, FlavorPost,ExceptionUser,ExceptionPost,LikeNotice,CommentNotice


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


        #评论通知
        CommentNotice.objects.create(
            user=post.author,
            post=post,
            post_title=post.title,
            which_comment=1,
            timestamp=time.time(),
        )
        return JsonResponse(get_comment_data(comment))
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})

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
        #评论通知
        CommentNotice.objects.create(
            user=parent_comment.user,
            post=parent_comment.post_id,
            post_title=parent_comment.post_id.title,
            which_comment=2,
            timestamp=time.time(),
        )
        return JsonResponse('code:200')
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})
def get_comment_data(comment):
    replies = [get_comment_data(reply) for reply in comment.replies.all()]
    return {
        'content': comment.content,
        'created_at': comment.comment_time.isoformat(),
        'author': comment.user.username,
        'replies': replies
    }

def comment_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = [get_comment_data(comment) for comment in post.comments.filter(parent_comment=None)]
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
    return JsonResponse(comments)

#点赞评论
@check_token
def like_comment(request, comment_id):
    if request.method == "POST":
        comment = Comment_for_post.objects.get(id=comment_id)
        comment.like_count += 1
        comment.user.exp += 1
        comment.user.save()
        request.myuser.exp += 1
        request.myuser.save()
        comment.save()
        LikeNotice.objects.create(
            user=comment.user,
            which_like=1,  # 根据你的定义，3 代表评论
            post=comment.post_id,
            post_title=comment.post_id.title,
            timestamp=time.time()
        )
        return JsonResponse('code:200')
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})

#举报评论
@check_token
def report_comment(request, comment_id):
    json_str = request.body.decode()
    data = json.loads(json_str)
    reason = data.get('reason')
    if request.method == "POST":
        comment = Comment_for_post.objects.get(id=comment_id)
        comment.report_count += 1
        author = comment.user
        post_id=comment.post_id
        post=Post.objects.get(id=post_id)
        ExceptionPost.objects.create(post_id=post,author=author,exception_reason=reason)
        ExceptionUser.objects.create(user=author,exception_reason="评论被举报",timestamp=time.time())
        comment.save()

        return JsonResponse('code:200')
    else:
        return JsonResponse({'code': 10200, 'error': '请求方式错误'})


#获取指定id的评论
def get_comment(request, comment_id):
    comment = Comment_for_post.objects.get(id=comment_id)
    return JsonResponse(get_comment_data(comment))