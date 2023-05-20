from django.urls import path

from post import views

urlpatterns =[
    path('<str:authorName>/post', views.post),
    path('<str:authorName>/delete', views.delete),
    path('<str:authorName>/get_all', views.get_all_posts),
    path('<str:authorName>/get_all_by_time', views.get_all_posts_by_time),
    path('<str:authorName>/get_post_by_like', views.get_posts_by_like),
    path('<str:authorName>/get_post_by_keyword', views.post),
    path('<str:authorName>/', views.post),
    path('<str:authorName>/', views.post),
]