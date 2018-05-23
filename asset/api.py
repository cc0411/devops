# -*- coding:utf-8 -*-

from rest_framework import viewsets
from asset.serializers import AssetInfoSerializer,HostGroupSerializer,HostUserSerializer,IDCSerializer
from asset.models import Assets,HostUsers,HostGroup,IDC

class AssetInfoViewSet(viewsets.ModelViewSet):
    queryset = Assets.objects.all()
    serializer_class = AssetInfoSerializer
class IDCViewSet(viewsets.ModelViewSet):
    queryset = IDC.objects.all()
    serializer_class = IDCSerializer
class HostUserViewSet(viewsets.ModelViewSet):
    queryset = HostUsers.objects.all()
    serializer_class = HostUserSerializer


class HostGroupViewSet(viewsets.ModelViewSet):
    queryset = HostGroup.objects.all()
    serializer_class = HostGroupSerializer