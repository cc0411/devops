# -*- coding:utf-8 -*-
from django.conf.urls import  url

from tasks import  views


urlpatterns = [
   url(r'^host_mgr/cmd/$', views.host_mgr,name='batch_cmd'),
   url(r'^host_mgr/file_transfer/$', views.file_transfer,name='file_transfer'),
   url(r'^batch_task_mgr/$', views.batch_task_mgr,name='batch_task_mgr'),
   url(r'^task_result/$', views.task_result,name='get_task_result'),
   url(r'^task_log/$',views.TasklogList.as_view(),name='task_log'),
   ]