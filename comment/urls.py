from django.urls import path

from comment import views

urlpatterns =[
    path('<int:post_id>/post/', views.create_comment_for_post),
    path('<int:comment_id>/comment/', views.create_comment_for_comment),
    path('<int:post_id>/get_all_comment/', views.comment_detail),
    path('<int:comment_id>/like/', views.like_comment),
    path('<int:comment_id>/report/', views.report_comment),
    path('<int:comment_id>/get_comment_by_id/', views.get_comment, name='get_comment_by_id'),

]