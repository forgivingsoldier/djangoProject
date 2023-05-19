from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from user.models import Post,Comment_for_post

def get_comment_data(comment):
    replies = [get_comment_data(reply) for reply in comment.replies.all()]
    return {
        'id': comment.id,
        'content': comment.content,
        'created_at': comment.created_at.isoformat(),
        'author': comment.author.username,
        'replies': replies
    }

def post_detail(request, post_id):
    post = Post.objects.get(post=post_id)
    comments = [get_comment_data(comment) for comment in post.comments.filter(parent_comment=None)]
    data = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at.isoformat(),
        'author': post.author.username,
        'comments': comments
    }
    return JsonResponse(data)
