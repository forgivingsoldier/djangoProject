import datetime

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.views import View

from tools.user_dec import check_token
from user.models import Resource, ExceptionResource, FlavorResource
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
import os
from datetime import datetime
# class sourceViews(View):
@method_decorator(check_token)
def post(request):

    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'code': 400, 'error': 'No file uploaded'})

    name = request.POST.get('name')
    author = request.POST.get('author')
    description = request.POST.get('description')
    subject = request.POST.get('subject')
    # file_url = request.POST.get('file_url')
    filetype = os.path.splitext(file.name)[1]  # Get the extension of the file
    # filetype = filetype.lstrip('.')
    if not all([name, author, description, subject]):
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})

    Resource.objects.create(
        name=name,
        author=author,
        description=description,
        subject=subject,
        # file_url=file_url,
        filetype=filetype,
        file=file,
        report_count=0
        # user=request.user
    )

    return JsonResponse({'code': 200, 'message': 'File uploaded successfully'})

@method_decorator(check_token)
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

@method_decorator(check_token)
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

    return FileResponse(file)

def get_subject(request):
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    subject = json_obj['subject']
    if subject:
        resources = Resource.objects.filter(subject=subject)
        if resources:
            # 我们只返回资源的名字
            resource_names = [resource.name for resource in resources]
            return JsonResponse({'code': 200, 'resource_names': resource_names})
        else:
            return JsonResponse({'code': 400, 'error': 'No resources found for this subject'})
    else:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})

# @method_decorator(check_token,name='get_filetype')
def get_filetype(request):
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    filetype = json_obj['filetype']
    if filetype:
        resources = Resource.objects.filter(filetype=filetype)
        if resources:
            # 我们只返回资源的名字
            resource_names = [resource.name for resource in resources]
            return JsonResponse({'code': 200, 'resource_names': resource_names})
        else:
            return JsonResponse({'code': 400, 'error': 'No resources found for this filetype'})
    else:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})

def get_author(request):
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    author = json_obj.get('author')
    if author:
        resources = Resource.objects.filter(author=author)
        if resources:
            # 我们只返回资源的名字
            resource_names = [resource.name for resource in resources]
            return JsonResponse({'code': 200, 'resource_names': resource_names})
        else:
            return JsonResponse({'code': 400, 'error': 'No resources found for this author'})
    else:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})

def download(request):
    json_str = request.body.decode()
    json_obj = json.loads(json_str)
    name = json_obj.get('name')
    if name:
        try:
            resource = Resource.objects.get(name=name)
            file = resource.file.path
            response = FileResponse(open(file, 'rb'))
            # provide the file name for download
            response['Content-Disposition'] = 'attachment; filename="%s"' % resource.file.name
            FlavorResource.objects.create(user=request.user,resource_id=resource.id, flavor_title=name, timestamp=datetime.now())
            return response
        except Resource.DoesNotExist:
            return JsonResponse({'code': 404, 'error': 'File not found'})
    else:
        return JsonResponse({'code': 400, 'error': 'Missing required fields'})

def report(request):
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
    ExceptionResource.objects.create(post_id=id, exception_reason=reason)
    return JsonResponse({'code': 200, 'message': 'Report submitted successfully'})
