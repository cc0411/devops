#-*- coding:utf-8 -*-

from django.forms import Form,ModelForm,fields,widgets
from .models import Tools, Variable


class ToolsForm(ModelForm):
    class Meta:
        model = Tools
        fields = '__all__'
        widgets = {
            'name':widgets.TextInput(attrs={'class': 'form-control',}),
            'comment': widgets.Textarea(attrs={'class': 'form-control','cols': 80, 'rows': 6}),
            'tool_script': widgets.Textarea(attrs={'class': 'form-control','cols': 80, 'rows': 6}),
            'tool_run_type': widgets.Select(attrs={'class': 'form-control','data-placeholder': '选择脚本类型'}),
        }

        help_texts = {
            'name': "*必填项目,名字不可以重复",
            'tool_script': '* python脚本 开头必须要写 #!/usr/bin/python',
        }


class VarsForm(ModelForm):
    class Meta:
        model = Variable
        fields = '__all__'
        widgets = {
            'name':widgets.TextInput(attrs={'class': 'form-control',}),
            'desc': widgets.Textarea(attrs={'class': 'form-control','cols': 80, 'rows': 6}),
            'vars': widgets.Textarea(attrs={'class': 'form-control','cols': 80, 'rows': 6}),
            'assets': widgets.SelectMultiple(attrs={'class': 'form-control','data-placeholder': '选择脚本类型'}),
        }

        help_texts = {
            'name': '* 必填项目,名字不可以重复,使用方法:在下面定义一个 path,  关联相关主机  在命令行 输入 echo {{ path }} 即可调用',
            'vars': '例如： {"path": "/tmp","name":"123"} , 默认变量  "hostname","inner_ip","network_ip","project"', }