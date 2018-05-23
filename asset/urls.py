# -*- coding:utf-8 -*-
from django.conf.urls import url
from asset import  views

urlpatterns = [
    url(r'^asset_list$',views.AssetList.as_view(),name='asset_list'),
    url(r'^idc_list$',views.IdcList.as_view(),name='idc_list'),
    url(r'^role_list$',views.HostGroupList.as_view(),name='role_list'),
    url(r'^user_list$',views.HostUserList.as_view(),name='user_list'),
    url(r'^idc_add$',views.IdcAdd.as_view(),name='idc_add'),
    url(r'^role_add$',views.GostGroupAdd.as_view(),name='role_add'),
    url(r'^asset_add$',views.AssetAdd.as_view(),name='asset_add'),
    url(r'^user_add$',views.HostUserAdd.as_view(),name='user_add'),
    url(r'idc_edit/(?P<pk>\d+)$',views.IdcUpdate.as_view(),name='idc_edit'),
    url(r'user_edit/(?P<pk>\d+)$',views.HostUserUpdate.as_view(),name='user_edit'),
    url(r'role_edit/(?P<pk>\d+)$',views.HostGroupUpdate.as_view(),name='role_edit'),
    url(r'^asset_edit/(?P<pk>\d+)$',views.AssetUpdate.as_view(),name='asset_edit'),
    url(r'^asset_del$',views.AssetDel.as_view(),name='asset_del'),
    url(r'^export$', views.export, name='export'),
    url(r'^idc_asset/nid(\d+)$', views.idc_asset, name="idc_asset"),
    url(r'^group_asset/nid(\d+)$', views.group_asset, name="group_asset"),


]