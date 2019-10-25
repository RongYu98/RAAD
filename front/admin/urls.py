from django.urls import path
from . import views, api

urlpatterns = [
    #views
    path('', views.home, name='home'),
    path('admin/', views.admin, name='admin'),
    #api
    path('login/', api.login, name='login'),
    path('logout/', api.logout, name='logout'),
]
