from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from user.models import Post, FlavorPost, FlavorResource,Resource
from tools.recommender import ContentBasedRecommender
import pandas as pd

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

    return JsonResponse({'recommended_posts': recommended_post_ids})

def recommend_resource_for_user(request, userName):
    try:
        flavor_logs = FlavorResource.objects.filter(user=userName)
    except ObjectDoesNotExist:
        #进行随机推荐
        resources = Resource.objects.all()
        resources_df = pd.DataFrame(resources.values('id', 'title'))
        recommender = ContentBasedRecommender(resources_df)
        recommended_resource_ids = recommender.recommend_items([], 5)
        return JsonResponse({'recommended_resources': recommended_resource_ids})

    # 获取用户浏览的所有内容的id
    resource_ids = [log.resource.id for log in flavor_logs]

    # 获取所有的内容和标题
    resources = Resource.objects.all()
    resources_df = pd.DataFrame(resources.values('id', 'title'))

    # 创建推荐器
    recommender = ContentBasedRecommender(resources_df)

    # 获取推荐的内容id
    recommended_resource_ids = recommender.recommend_items(resource_ids, 5)

    return JsonResponse({'recommended_resources': recommended_resource_ids})

