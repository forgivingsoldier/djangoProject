import datetime

import pandas as pd
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.db.models import Count, Q
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from tools.recommender import ContentBasedRecommender
from tools.user_dec import check_token
from user.models import Resource, ExceptionResource, FlavorResource, LikeNotice, User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
import os
from datetime import datetime
# class sourceViews(View):
@check_token
def post(request):
    writer = request.myuser
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'code': 400, 'error': 'No file uploaded'})

    name = request.POST.get('name')
    # author = request.POST.get('author')
    description = request.POST.get('description')
    subject = request.POST.get('subject')
    filetype = os.path.splitext(file.name)[1].replace('.', '')  # Get the extension of the file

    # Check if a resource with the same name already exists
    if Resource.objects.filter(name=name).exists():
        return JsonResponse({'code': 400, 'error': 'A resource with this name already exists'})

    if not all([name, description, subject]):
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})

    file_name = default_storage.save(file.name, file)
    file_size = os.path.getsize(default_storage.path(file_name))
    new_resource = Resource.objects.create(
        name=name,
        author=writer.username,
        description=description,
        subject=subject,
        filetype=filetype,
        file=file,
        report_count=0,
        file_size=file_size
    )

    upload_time = new_resource.upload_time
    return JsonResponse({
        'code': 200, 'message': 'File uploaded successfully',
        'upload_time': upload_time.strftime("%Y-%m-%d %H:%M:%S")
    })

#@check_token
def delete(request):
    # if not request.user.is_authenticated:
    #     return JsonResponse({'code': 403, 'error': 'Not authorized'})
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    name = json_obj['name']
    try:
        resource = Resource.objects.get(name=name)
    except ObjectDoesNotExist:
        return JsonResponse({'code': 400, 'error': 'Resource not found'})

    # Delete the resource
    resource.delete()
    return JsonResponse({'code': 200, 'message': 'Resource deleted successfully'})

# @check_token
def get(request):
    # Try to get the requested resource
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    name = json_obj['name']
    try:
        resource = Resource.objects.get(name=name)
    except Resource.DoesNotExist:
        return JsonResponse({'code': 404, 'error': 'Resource not found'})

    # Open the file and return its content as a response
    try:
        file = open(resource.file.path, 'rb')
    except Exception as e:
        return JsonResponse({'code': 500, 'error': 'Error opening the file'})
    response = FileResponse(file)

    # Set the Content-Type based on the file type
    # This is just an example, you should set the Content-Type based on your actual file type
    if resource.filetype == 'txt':
        response['Content-Type'] = 'text/plain'
    elif resource.filetype == 'jpg':
        response['Content-Type'] = 'image/jpeg'
    # and so on for other file types...
    elif resource.filetype == 'png':
        response['Content-Type'] = 'image/png'
    elif resource.filetype == 'pdf':
        response['Content-Type'] = 'application/pdf'
    return response
    # return FileResponse(file)
#@check_token
def get_writer(request):
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    author = json_obj['author']
    if author:
        resources = Resource.objects.filter(author=author)
        if resources:
            # 我们返回一个包含所有资源信息的列表
            resource_info_list = []
            for resource in resources:
                resource_info = {
                    'name': resource.name,
                    'author': resource.author,
                    'subject': resource.subject,
                    'description': resource.description,
                    'upload_time': resource.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
                }
                resource_info_list.append(resource_info)

            return JsonResponse({'code': 200, 'resource_info_list': resource_info_list})
        else:
            return JsonResponse({'code': 400, 'error': 'No resources found for this author'})
    else:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})
def get_subject(request):
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    subject = json_obj['subject']
    if subject:
        resources = Resource.objects.filter(subject=subject)
        if resources:
            # 我们返回一个包含所有资源信息的列表
            resource_info_list = []
            for resource in resources:
                resource_info = {
                    'name': resource.name,
                    'author': resource.author,
                    'subject': resource.subject,
                    'description': resource.description,
                    'upload_time': resource.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
                }
                resource_info_list.append(resource_info)

            return JsonResponse({'code': 200, 'resource_info_list': resource_info_list})
        else:
            return JsonResponse({'code': 400, 'error': 'No resources found for this subject'})
    else:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})
#@check_token
# @method_decorator(check_token,name='get_filetype')
def get_filetype(request):
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    filetype = json_obj['filetype']
    if filetype:
        resources = Resource.objects.filter(filetype=filetype)
        if resources:
            # 我们返回一个包含所有资源信息的列表
            resource_info_list = []
            for resource in resources:
                resource_info = {
                    'name': resource.name,
                    'author': resource.author,
                    'subject': resource.subject,
                    'description': resource.description,
                    'upload_time': resource.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
                }
                resource_info_list.append(resource_info)

            return JsonResponse({'code': 200, 'resource_info_list': resource_info_list})
        else:
            return JsonResponse({'code': 400, 'error': 'No resources found for this filetype'})
    else:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})
@check_token
def get_author(request):
    # author = request.myuser
    # # if author:
    # #     resources = Resource.objects.filter(author=author)
    # #     if resources:
    # #         # 我们只返回资源的名字
    # #         resource_data = [{
    # #             'name': resource.name,
    # #             'author': author.username,  # Assuming author is an User instance
    # #             'subject': resource.subject,
    # #             'description': resource.description,
    # #             'file_size': f"{round(resource.file_size/1024)}KB",
    # #             'upload_time': resource.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
    # #         } for resource in resources]
    # #         return JsonResponse({'code': 200, 'resources': resource_data})
    # #     else:
    # #         return JsonResponse({'code': 400, 'error': 'No resources found for this author'})
    # # else:
    # #     return JsonResponse({'code': 400, 'error': 'Missing required fields'})
    # if author:
    #     resources = Resource.objects.filter(author=author)
    #     if resources:
    #         resource_info_list = []
    #         for resource in resources:
    #             resource_info = {
    #                 'name': resource.name,
    #                 'author': author.username,
    #                 'subject': resource.subject,
    #                 'description': resource.description,
    #                 'upload_time': resource.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
    #             }
    #             resource_info_list.append(resource_info)
    #
    #         return JsonResponse({'code': 200, 'resource_info_list': resource_info_list})
    #     else:
    #         return JsonResponse({'code': 400, 'error': 'No resources found for this author'})
    # else:
    #     return JsonResponse({'code': 400, 'error': 'Author does not exist'})
    # json_str = request.body.decode()
    # json_obj = json.loads(json_str)
    # author = json_obj.get('author')
    author=request.myuser
    author_name=author.username
    if author_name:
        resources = Resource.objects.filter(author=author_name)
        if resources:
            resource_info_list = []
            for resource in resources:
                resource_info = {
                    'name': resource.name,
                    'author': resource.author,
                    'subject': resource.subject,
                    'description': resource.description,
                    'upload_time': resource.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
                }
                resource_info_list.append(resource_info)

            return JsonResponse({'code': 200, 'resource_info_list': resource_info_list})
        else:
            return JsonResponse({'code': 400, 'error': 'No resources found for this author'})
    else:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})
#@check_token
def get_name(request):
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    name = json_obj.get('name')
    if name:
        # Perform a case-insensitive wildcard match
        resources = Resource.objects.filter(Q(name__icontains=name))
        if resources:
            resource_info_list = []
            for resource in resources:
                resource_info = {
                    'name': resource.name,
                    'author': resource.author,
                    'subject': resource.subject,
                    'description': resource.description,
                    'upload_time': resource.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
                }
                resource_info_list.append(resource_info)

            return JsonResponse({'code': 200, 'resource_info_list': resource_info_list})
        else:
            return JsonResponse({'code': 400, 'error': 'No resources found with this name'})
    else:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})
@check_token
def download(request):
    user = request.myuser
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    name = json_obj.get('name')
    if name:
        try:
            resource = Resource.objects.get(name=name)
            file = resource.file.path
            response = FileResponse(open(file, 'rb'))
            # provide the file name for download
            # response['Content-Type'] = 'text/plain; charset=utf-8'
            if resource.filetype == 'txt':
                response['Content-Type'] = 'text/plain; charset=utf-8'
            elif resource.filetype == 'pdf':
                response['Content-Type'] = 'application/pdf'
            elif resource.filetype == 'txt':
                response['Content-Type'] = 'text/plain; charset=utf-8'
            elif resource.filetype == 'png':
                response['Content-Type'] = 'image/png'
            response['Content-Disposition'] = 'attachment; filename="%s"' % resource.file.name
            FlavorResource.objects.create(user=user, resource_id=resource, flavor_title=name, timestamp=datetime.now())
            return response
        except Resource.DoesNotExist:
            return JsonResponse({'code': 404, 'error': 'File not found'})
    else:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})
@check_token
def report(request):
    # 获取当前用户
    user = request.myuser

    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    name = json_obj.get('name')
    reason = json_obj['reason']
    if not name:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})

    resource = Resource.objects.filter(name=name).first()
    if not resource:
        return JsonResponse({'code': 400, 'error': 'Resource not found'})

    resource.report_count += 1
    resource.save()

    # 创建 ExceptionResource 对象，同时记录下 author 和 source_id
    ExceptionResource.objects.create(author=user, source_id=resource, exception_reason=reason)

    return JsonResponse({'code': 200, 'message': 'Report submitted successfully'})
# @check_token
# def recommend_resource_for_user(request):
#     # 假设我们接收一个 JSON 请求，包含用户的 username
#     # json_str = request.body.decode()
#     # json_obj = json.loads(json_str)
#     # username = json_obj.get('username')
#     author=request.myuser
#     author_name=author.username
#     # 获取该用户最喜欢的资源标题
#     try:
#         flavor = FlavorResource.objects.filter(user=author_name).order_by('-timestamp').first()
#         if not flavor:
#             return JsonResponse({'code': 400, 'error': 'User does not have any flavor'})
#
#         flavor_title = flavor.flavor_title
#     except FlavorResource.DoesNotExist:
#         return JsonResponse({'code': 400, 'error': 'FlavorResource not found'})
#
#     # 获取具有相同标题的资源
#     resources = Resource.objects.filter(name=flavor_title)
#
#     # 我们只返回资源的名字
#     resource_names = [resource.name for resource in resources]
#
#     return JsonResponse({'code': 200, 'resource_names': resource_names})
# @check_token
# def recommend_resource_for_user(request):
#     user=request.myuser
#     try:
#         flavor_logs = FlavorResource.objects.filter(user=user.username)
#     except ObjectDoesNotExist:
#         # 进行随机推荐
#         resources = Resource.objects.all()
#         resources_df = pd.DataFrame(resources.values('id', 'name'))
#         recommender = ContentBasedRecommender(resources_df)
#         recommended_resource_ids = recommender.recommend_items([], 5)
#         return JsonResponse({'recommended_resources': recommended_resource_ids})
#     # 获取用户浏览的所有内容的id
#     resource_ids = [log.resource_id for log in flavor_logs]
#
#     # 获取所有的内容和标题
#     resources = Resource.objects.all()
#     resources_df = pd.DataFrame(resources.values('id', 'name'))
#
#     # 创建推荐器
#     recommender = ContentBasedRecommender(resources_df)
#
#     # 获取推荐的内容id
#     recommended_resource_ids = recommender.recommend_items(resource_ids, 5)
#     recommended_posts = [
#         {
#             "id": resource_id,
#             "name": resources.get(id=resource_id).name,
#             "url": reverse('get_resource_by_id', args=[resource_id]),
#         }
#         for resource_id in recommended_resource_ids
#     ]
#     return JsonResponse({'recommended_resources': recommended_posts})
@check_token
def recommend_resource_for_user(request):
    user = request.myuser
    author_name=user.username
    # 获取用户下载过的所有资源的标题
    user_downloads = FlavorResource.objects.filter(user=author_name)
    downloaded_titles = [flavor_resource.flavor_title for flavor_resource in user_downloads]

    # 查找具有类似标题的资源
    query = Q()
    for title in downloaded_titles:
        query |= Q(name__icontains=title)  # 使用icontains实现模糊匹配

    # 使用distinct()来避免重复的推荐
    recommended_resources = Resource.objects.filter(query).distinct()
    if not recommended_resources:
        # return JsonResponse({'code': 400, 'error': 'No similar resources found'})
        recommended_resources = Resource.objects.order_by('?')[:5]  # 随机选择 5 个资源
    if recommended_resources:
        resource_data = [{
            'name': resource.name,
            'author': resource.author,  # Assuming author is an User instance
            'subject': resource.subject,
            'description': resource.description,
            #'file_size': f"{round(resource.file_size / 1024)}KB",
            'upload_time': resource.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
        } for resource in recommended_resources]
        return JsonResponse({'code': 200, 'resources': resource_data})
    else:
        return JsonResponse({'code': 400, 'error': 'No similar resources found'})


