from django.urls import path, re_path
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
    path('add_ip/', api.add_ip, name='add_ip'),
    re_path(r'^del_ip/(?P<ip>[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})/$', api.del_ip, name='del_ip'),
    path('password/', api.password, name='api_password'),
]

