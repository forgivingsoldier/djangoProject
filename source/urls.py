# from django.urls import path
from source import views
# from source.views import sourceViews
#
# urlpatterns =[
#     # path('', views.sourceViews.as_view()),
#     # path('source/<str:name>/', sourceViews.as_view()),
#     path('<str:name>/', views.sourceViews.as_view()),
# ]
from django.urls import path
# from .views import sourceViews

urlpatterns = [
    # path('source/<str:name>/', sourceViews.as_view()),
    path('post', views.post),
    path('delete', views.delete),
    path('get', views.get),
    path('get_subject', views.get_subject),
    path('get_filetype', views.get_filetype),
    path('get_author', views.get_author),
    # path('get_writer', views.get_writer),
    path('download', views.download),
    path('report', views.report),
    path('get_name',views.get_name),
    path('get_writer',views.get_writer),
    path('recommend_resource_for_user', views.recommend_resource_for_user)
]