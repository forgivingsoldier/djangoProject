from django.urls import path

from comment import views

urlpatterns =[
    path('<int:post_id>/post/', views.create_comment_for_post),
    path('<int:comment_id>/comment/', views.create_comment_for_comment),
    path('<int:post_id>/get_all/', views.post_detail),
]