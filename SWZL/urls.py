from django.conf.urls import url, include
from django.contrib import admin
from SWZL import views

urlpatterns = [
    # 发布信息
    url(r'^recruit/$', views.recruit, name='recruit'),
    # 失物招领列表的显示
    url(r'^recruit_list/$', views.RecruitList.as_view(), name='recruit_list'),
    # 失物信息的展示
    url(r'^lost_list/$', views.LostList.as_view(), name='lost_list'),
    # 招领信息的显示
    url(r'^find_list/$', views.FindList.as_view(), name='find_list'),
    # 失物的详细信息
    url(r'^lost_detail_view/(?P<info_id>\d+)/$', views.lost_detail_view, name='lost_detail_view'),
    # 招领的详细信息
    url(r'^find_detail_view/(?P<info_id>\d+)/$', views.find_detail_view, name='find_detail_view'),
]
