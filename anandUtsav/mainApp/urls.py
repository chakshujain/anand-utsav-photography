from django.contrib import admin
from django.urls import path, include

from .views import *
urlpatterns = [
    path('upload-images', uploadImage, name='upload-images'),
    path('success', success, name='success'),
    path('display-images', displayImages, name='display-images')
]
