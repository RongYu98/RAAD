from django.urls import path, re_path
from . import views, api

urlpatterns = [
    #views
    path('admin/', views.home, name='home'),
    path('admin/blacklist/', views.blacklist, name='blacklist'),
    path('admin/threshold/', views.threshold, name='threshold'),
    path('admin/password/', views.password, name='password'),
    path('error/', views.error, name='error'),
    #api
    path('signin/', api.signin, name='signin'),
    path('signout/', api.signout, name='signout'),
    path('blacklist_ip/', api.blacklist_ip, name='blacklist_ip'),
    re_path(r'^remove_blacklisted_ip/(?P<ip>[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})/$', api.remove_blacklisted_ip, name='remove_blacklisted_ip'),
    path('set_threshold/', api.set_threshold, name='set_threshold'),
    path('password/', api.password, name='api_password'),
]

