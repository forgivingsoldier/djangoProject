# user/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('sms', views.sms_view),
    path('<str:username>/change_password', views.change_password),
    path('<str:username>/change_password_by_phone', views.change_password_by_phone),

    path('<str:username>/info', views.info),
    path('<str:username>/get_avatar', views.get_avatar, name='get_avatar'),
    path('<str:username>/change_info', views.change_info),
    path('<str:username>/change_avatar', views.change_avatar),
    path('<str:username>/logout', views.logout),
    path('<str:username>/delete_account', views.delete_account),
    path('online_num', views.get_online_user_num),
    path('<str:username>/check_level', views.check_level),
    path('<str:username>/admin_apply', views.apply_admin),
    path('<str:username>/follow', views.follow),
    path('<str:username>/unfollow', views.unfollow),
    path('<str:username>/get_liked', views.get_all_liked),
    path('<str:username>/get_commented', views.get_all_commented),
    path('<str:username>/get_follow_num', views.get_follow_num),
    path('<str:username>/get_fans_num', views.get_fans_num),


]

