from django.urls import path

from post import views

urlpatterns =[
    path('<str:authorName>/', views.postViews.as_view()),
]