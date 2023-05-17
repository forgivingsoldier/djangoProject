# user/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('<str:username>/info', views.info),
    path('<str:username>/change_info', views.change_info),
    path('<str:username>/change_avatar', views.change_avatar),
    path('<str:username>/change_password', views.change_password),
]

