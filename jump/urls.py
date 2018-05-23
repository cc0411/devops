# -*- coding:utf-8 -*-

from  django.conf.urls import  url
from jump import views


urlpatterns = [
    url(r'^$',views.Index.as_view(),name='terminal'),
    url(r'^sshlogslist/$',views.SshLogList.as_view(),name='sshlogslist'),
    url(r'^sshterminalkill/$',views.SshTerminalKill.as_view(),name='sshterminalkill'),
    url(r'^sshlogplay/(?P<pk>[0-9]+)/',views.SshLogPlay.as_view(),name='sshlogplay'),
    url(r'^sshterminalmonitor/(?P<pk>[0-9]+)/',views.SshTerminalMonitor.as_view(),name='sshterminalmonitor'),
]


