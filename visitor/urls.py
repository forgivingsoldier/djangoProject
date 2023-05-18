from django.urls import path

from . import views
#from .views import VisitorViews

urlpatterns = [
    path('sms',views.sms_view),# 注册与用户名冲突
    path('register/',views.register)
]