# -*- coding:utf-8 -*-
from django.forms import Form,ModelForm,fields,widgets
from asset import models


class AssetUpForm(Form):
    file = fields.FileField(label="导入资产")

class HostGroupForm(ModelForm):
    class Meta:
        model = models.HostGroup
        fields = '__all__'
        error_messages = {
            'name': {'required': '名称不能为空',},
        }
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control',}),
            'servers': widgets.SelectMultiple(attrs={'class': 'form-control',}),
        }


class HostUserForm(ModelForm):
    class Meta:
        model = models.HostUsers
        fields = '__all__'
        error_messages = {
            'name': {'required': '名称不能为空',},
            'auth_method': {'required': '连接方式不能为空',},
            'username': {'required': '账户不能为空',},

        }
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control',}),
            'auth_method': widgets.Select(attrs={'class': 'form-control',}),
            'username': widgets.TextInput(attrs={'class': 'form-control',}),
            'password': widgets.TextInput(attrs={'class': 'form-control',}),

        }

class IDCForm(ModelForm):
    class Meta:
        model = models.IDC
        fields ='__all__'
        error_messages = {
            'name': {'required': '机房名称不能为空', },
        }
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control', }),
            'servers': widgets.SelectMultiple(attrs={'class': 'form-control',}),
        }


class AssetForm(ModelForm):
    class Meta:
        model = models.Assets
        fields = '__all__'
        error_message ={
            'hostname': {'required': '主机名不能为空',},
            'wip': {'required': '外网地址不能为空', 'invalid': 'IP地址格式错误'},
            'lip': {'required': '内网地址不能为空', 'invalid': 'IP地址格式错误'},
            'system_type': {'required': '系统类型不能为空'},
            'ssh_port': {'required': '端口不能为空', 'invalid': '格式错误,请输入数字'},


        }
        widgets = {
            'hostname': widgets.TextInput(attrs={'class': 'form-control',}),
            'lip': widgets.TextInput(attrs={'class': 'form-control',}),
            'wip': widgets.TextInput(attrs={'class': 'form-control',}),
            'cpu': widgets.TextInput(attrs={'class': 'form-control',}),
            'memory': widgets.TextInput(attrs={'class': 'form-control',}),
            'disk': widgets.TextInput(attrs={'class': 'form-control',}),
            'instance_id': widgets.TextInput(attrs={'class': 'form-control',}),
            'system_type': widgets.TextInput(attrs={'class': 'form-control',}),
            'user': widgets.Select(attrs={'class': 'form-control',}),
            'buy_time':widgets.DateTimeInput(attrs={'class':'form-control layer-date','placeholder':"YYYY-MM-DD hh:mm:ss","onclick":"laydate({istime: true, format: 'YYYY-MM-DD hh:mm:ss'})"}),
            'expire_time':widgets.DateTimeInput(attrs={'class':'form-control layer-date','placeholder':"YYYY-MM-DD hh:mm:ss","onclick":"laydate({istime: true, format: 'YYYY-MM-DD hh:mm:ss'})"}),
            'online_status': widgets.Select(attrs={'class': 'form-control'}),
            'ssh_port': widgets.TextInput(attrs={'class': 'form-control',}),
            'serverid': widgets.TextInput(attrs={'class': 'form-control',}),
            'gameid': widgets.TextInput(attrs={'class': 'form-control'}),
            'memo': widgets.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'hostname': '*  必填项目,名字唯一,主机名这里请不要写IP',
            'user': '创建资产前请先创建主机账户'
        }