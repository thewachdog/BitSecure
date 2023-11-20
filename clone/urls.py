from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('login.html', login),
    path('sign-up.html', signup),
    path('upload/', upload_video, name='upload_video'),
]
