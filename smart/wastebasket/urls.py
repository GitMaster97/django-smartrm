# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'wastebasket'
urlpatterns = [
    url(r'^$', views.home_page, name="home"),
    url(r'^wastebasket/$', views.wastebasket_list, name='wastebasket_list'),
    url(r'^wastebasket/(?P<pk>\d+)/$', views.wastebasket_detail, name='wastebasket_detail'),
    url(r'^wastebasket/new/$', views.wastebasket_new, name='wastebasket_new'),

    url(r'^task/$', views.task_list, name='task_list'),
    url(r'^task/(?P<pk>\d+)/$', views.task_detail, name='task_detail'),    
    url(r'^task/new/$', views.task_new, name='task_new'),
    url(r'^task/result/(?P<pk>\d+)/$', views.task_result, name='task_result'),
]

