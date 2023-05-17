from django.test import TestCase
from django.urls import path
from . import views
# Create your tests here.
urlpattern = [
    path('<str:authorName>', views.postViews.as_view()),
]