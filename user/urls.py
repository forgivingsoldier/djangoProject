# user/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('<str:username>/info', views.info),
]

