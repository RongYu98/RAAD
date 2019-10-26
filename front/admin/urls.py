from django.urls import path
from . import views, api

urlpatterns = [
    #views
    path('', views.home, name='home'),
    path('admin/blacklist/', views.blacklist, name='blacklist'),
    path('admin/threshold/', views.threshold, name='threshold'),
    path('admin/password/', views.password, name='password'),
    path('error/', views.error, name='error'),
    #api
    path('signin/', api.signin, name='signin'),
    path('signout/', api.signout, name='signout'),
    path('password/', api.password, name='api_password'),
]

