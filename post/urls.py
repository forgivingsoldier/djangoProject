from django.urls import path

from post import views

urlpatterns =[
    path('<str:authorName>/post', views.post),
    path('<str:authorName>/delete', views.delete),
    path('<str:authorName>/get_all', views.get_all_posts),
    path('<str:authorName>/get_all_by_time', views.get_all_posts_by_time),
    path('<str:authorName>/get_post_by_like', views.get_posts_by_like),
    path('<str:authorName>/get_post_by_keyword', views.post),
    path('<str:authorName>/get_post_by_comment', views.get_posts_by_comment),
    path('<str:authorName>/get_all_posts_by_like', views.get_all_posts_by_like),
    path('<str:authorName>/get_all_posts_by_comment', views.get_all_posts_by_comment),
    path('<str:authorName>/get_all_posts_by_time', views.get_all_posts_by_time),
    path('<str:authorName>/change_post', views.put),
    path('<str:authorName>/is_required', views.is_require_level),
    path('<str:authorName>/like', views.like),
    path('<str:authorName>/unlike', views.unlike),
    path('<str:authorName>/report', views.report),
    path('<str:authorName>/recommend', views.recommend_post_for_user),
    path('<int:id>/get_post_by_id', views.get_post_by_id,name='get_post_by_id'),
    path('<str:authorName>/get_follow_post', views.get_follow_post),

]