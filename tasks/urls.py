# -*- coding:utf-8 -*-
from django.conf.urls import  url

from . import  views


urlpatterns = [
   url(r'^host_mgr/cmd/$', views.host_mgr,name='batch_cmd'),
   url(r'^host_mgr/file_transfer/$', views.file_transfer,name='file_transfer'),
   url(r'^batch_task_mgr/$', views.batch_task_mgr,name='batch_task_mgr'),
   url(r'^task_result/$', views.task_result,name='get_task_result'),
   url(r'^task_log/$',views.TasklogList.as_view(),name='task_log'),
   url(r'^shell/$',views.TasksCmd.as_view(),name='shell'),
   url(r'^shellresult/$',views.TasksPerform.as_view(),name='shellresult'),
   url(r'^tools/$', views.ToolsList.as_view(), name='toolslist'),
   url(r'^tools_add/$', views.ToolsAdd.as_view(), name='tools_add'),
   url(r'^tools_del/$', views.ToolsAllDel.as_view(), name='tools_bulk_delete'),
   url(r'^tools_update/(?P<pk>\d+)$', views.ToolsUpdate.as_view(), name='tools_update'),
   url(r'^tools_exec/$', views.ToolsExec.as_view(), name='tools_exec'),

   url(r'^tools_results/$', views.ToolsResultsList.as_view(), name='tools_results'),
   url(r'^tools_result_detail/(?P<pk>\d+)$', views.ToolsResultsDetail.as_view(), name='tools_results_detail'),
   url(r'^var/$', views.VarsList.as_view(), name='varlist'),
   url(r'^vars_add/$', views.VarsAdd.as_view(), name='vars_add'),
   url(r'^vars_del/$', views.VarsAllDel.as_view(), name='vars_bulk_delete'),
   url(r'^vars_update/(?P<pk>\d+)$', views.VarsUpdate.as_view(), name='vars_update'),

   ]