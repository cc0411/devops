"""devops URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from index import  views
from asset.api import AssetInfoViewSet,HostGroupViewSet,HostUserViewSet,IDCViewSet
from rest_framework import routers
from django.conf import settings

router = routers.DefaultRouter()
router.register('hostgroup', HostGroupViewSet)
router.register('asset', AssetInfoViewSet)
router.register('hostuser', HostUserViewSet)
router.register('idc', IDCViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^$', views.index, name='index'),
    url(r'^dashboard', views.Dashboard, name='Dashboard'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^session/$', views.LoginLogList.as_view(), name='session'),
    url(r'^asset/', include('asset.urls'), ),
    url(r'^jump/', include('jump.urls'), ),
    url(r'^api/',include(router.urls)),
]

from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, { 'document_root': settings.MEDIA_ROOT, }),
    ]