from django.urls import path

from admin import views

urlpatterns = [
    path('login', views.admin_login),
    path('get_exception_users', views.get_exception_users),
    path('get_exception_comments', views.get_exception_comments),
    path('delete_exception_user', views.delete_exception_user),
    path('get_exception_posts', views.get_exception_posts),
   # path('get_exception_resources', views.get_exception_resources),
    path('get_admin_requests', views.get_admin_requests),
    path('handle_admin_requests', views.handle_admin_request),
    path('refuse_admin_requests', views.refuse_admin_request),
    path('delete_post', views.delete_post),
    path('delete_comment', views.delete_comment),
    path('ignore_exception_post', views.ignore_exception_post),
    path('ignore_exception_comment', views.ignore_exception_comment),
    path('ignore_exception_user', views.ignore_exception_user),
    path('warn_exception_user', views.warn_exception_user),
]