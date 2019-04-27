"""suzl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from SWZL import views
from django.views.static import serve

from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 用户注册
    url(r'^register/', views.register,name='register'),
    # 用户登录
    url(r'^login/', views.login),
    # 失物招领的发布
    url(r'swzl/', include('SWZL.urls', namespace='suzl')),
    # 图片上传的路径配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
