from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('login.html', views.login),
    path('sign-up.html', views.signup),

]