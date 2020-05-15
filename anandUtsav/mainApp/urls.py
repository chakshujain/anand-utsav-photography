from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('upload-images/<int:userId>/', uploadImage, name='upload-images'),
    path('new-user', createNewUser, name='new-user'),

    path('login', loginUser, name='login'),
    path('logout', logoutUser, name='logout'),
    path('services', services, name='services'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('gallery', gallery, name='gallery'),
    path('blog', blog, name='blog')
]
