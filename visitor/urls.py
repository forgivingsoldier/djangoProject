from django.urls import path

from . import views
#from .views import VisitorViews

urlpatterns = [
    path('register/',views.register)
]