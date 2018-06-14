# -*- coding:utf-8 -*-
from rest_framework import serializers
from asset.models import Assets,HostGroup,HostUsers,IDC

class AssetInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = '__all__'
        depth = 2

class HostGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HostGroup
        fields = '__all__'



class HostUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HostUsers
        fields = '__all__'

class IDCSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IDC
        fields = '__all__'