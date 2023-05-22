# user/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('<str:username>/info', views.info),
    path('<str:username>/change_info', views.change_info),
    path('<str:username>/change_avatar', views.change_avatar),
    path('<str:username>/change_password', views.change_password),
    path('<str:username>/logout', views.logout),
    path('<str:username>/delete_account', views.delete_account),
    path('<str:username>/change_password_by_phone', views.change_password_by_phone),
    path('sms', views.sms_view),
    path('online_num/', views.get_online_user_num),
    path('<str:username>/check_level', views.check_level),
    path('<str:username>/admin_apply', views.apply_admin),
    path('<str:username>/follow', views.follow),
    path('<str:username>/unfollow', views.unfollow),
    path('<str:username>/get_follow_likes', views.get_follow_likes),
    path('<str:username>/get_follow_comments', views.get_follow_comments),


]

