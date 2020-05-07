from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('upload-images/<int:userId>/', uploadImage, name='upload-images'),
    path('images', displayImages, name='display-images'),
    path('new-user', createNewUser, name='new-user'),
    path('login', loginUser, name='login'),
    path('logout', logoutUser, name='logout')
]
