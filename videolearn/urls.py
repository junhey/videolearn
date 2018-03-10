"""videolearn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from video import views
from django.urls import path
from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('',views.index,name='index'),
    
    re_path(r'^video/(?P<vid>\d+)/$',views.videoDetail, name='videoDetail'),
    path('history/', views.viewHistory, name="viewHistory"),
    path('cate/<int:cateid>/',views.videoCate, name='videoCate'),
    path('login/', views.logIn, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logOut, name="logout"),
    path('admin/', admin.site.urls),    
    path('like/',views.like, name='like'),
    path('check_code',views.check_code,name='check_code'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}, name='media'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT,}, name='static'),
    
]
urlpatterns += staticfiles_urlpatterns()