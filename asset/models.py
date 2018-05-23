# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
# Create your models here.

class IDC(models.Model):
    name = models.CharField(max_length=32,unique=True,verbose_name=u'机房名')
    servers = models.ManyToManyField('Assets')
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return  self.name
    class Meta:
        db_table = 'idc'
        verbose_name = u'机房'
        verbose_name_plural = u'机房'
        permissions ={
            ("can_add_idc", ("可以添加机房")),
            ("can_change_idc", ("可以修改机房信息")),
            ("can_delete_idc", ("可以删除机房")),
            ("can_view_idc", ("可以查看机房信息")),

        }

class Assets(models.Model):
    hostname = models.CharField(max_length=32,unique=True,verbose_name=u'主机名',)
    wip = models.GenericIPAddressField(unique=True,verbose_name=u'外网IP')
    lip = models.GenericIPAddressField(unique=True,verbose_name=u'内网IP')
    system_type = models.CharField(max_length=64,blank=True,null=True,verbose_name=u'系统类型')
    ssh_port = models.IntegerField(default=22,verbose_name='ssh端口')
    cpu = models.CharField(max_length=64,blank=True,null=True,verbose_name=u'CPU')
    memory = models.CharField(max_length=64,blank=True,null=True,verbose_name=u'内存')
    disk = models.CharField(max_length=64,blank=True,null=True,verbose_name=u'硬盘')
    instance_id = models.CharField(max_length=64,null=True,blank=True,verbose_name=u'实例ID')
    buy_time = models.DateTimeField(verbose_name='购买时间', null=True, blank=True)
    expire_time = models.DateTimeField(verbose_name='到期时间', null=True, blank=True)
    online_choices = (
        (0,'上线'),
        (1,'下线'),
    )
    user = models.ForeignKey('HostUsers',verbose_name=u'系统用户')
    online_status = models.SmallIntegerField(choices=online_choices,verbose_name=u'状态')
    serverid = models.IntegerField(blank=True, null=True,verbose_name=u'ServerID')
    gameid = models.IntegerField(blank=True, null=True,verbose_name=u'GameID')
    ctime = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    utime= models.DateTimeField(auto_now=True,verbose_name=u'修改时间')
    memo = models.CharField(max_length=256,blank=True,null=True,verbose_name=u'备注')
    def __str__(self):
        return self.hostname

    def gethostname(self):
        return slugify(self.hostname)
    class Meta:
        db_table = 'assets'
        verbose_name_plural = u'资产'
        verbose_name = u'资产'
        permissions = {
            ("can_add_asset", ("可以添加资产")),
            ("can_change_asset", ("可以修改资产")),
            ("can_delete_asset", ("可以删除资产")),
            ("can_connect_asset", ("可以连接终端")),
            ("can_kill_asset", ("可以关闭终端")),
            ("can_monitor_asset", ("可以监控终端")),
            ("can_view_asset", ("可以查看资产")),

        }
class HostUsers(models.Model):
    name = models.CharField(max_length=32,unique=True,verbose_name=u'名称')
    auth_method_choices = (('ssh-password', "SSH/ Password"), ('ssh-key', "SSH/KEY"))
    auth_method = models.CharField(choices=auth_method_choices, max_length=16,
                                   help_text='如果选择SSH/KEY，请确保你的私钥文件已在settings.py中指定',verbose_name=u'类型')
    username = models.CharField(max_length=32,verbose_name=u'用户名')
    password = models.CharField(verbose_name=u'密码',max_length=64, blank=True, null=True, help_text='如果auth_method选择的是SSH/KEY,那此处不需要填写..')
    key = models.TextField(blank=True)
    memo = models.CharField(max_length=128, blank=True, null=True,verbose_name=u'备注')
    width = models.PositiveIntegerField(verbose_name='width', default=1024)
    height = models.PositiveIntegerField(verbose_name='height', default=768)
    dpi = models.PositiveIntegerField(verbose_name='dpi', default=96)
    def __str__(self):
        return '%s----%s' % (self.name, self.username)

    def clean(self):

        if self.auth_method == 'password' and len(self.password) == 0:
            raise ValidationError('If you choose password auth method,You must set password!')
        if self.auth_method == 'password' and len(self.key) > 0:
            raise ValidationError('If you choose password auth method,You must make key field for blank!')
        if self.auth_method == 'key' and len(self.key) == 0:
            raise ValidationError('If you choose key auth method,You must fill in key field!')
        if self.auth_method == 'key' and len(self.password) > 0:
            raise ValidationError('If you choose key auth method,You must make password field for blank!')

    class Meta:
        db_table = 'hostusers'
        verbose_name = '远程用户'
        verbose_name_plural = '远程用户'
        unique_together = ('auth_method', 'password', 'username')
        permissions = (
            ("can_add_hostuser", ("可以添加服务器用户信息")),
            ("can_change_hostuser", ("可以修改服务器用户信息")),
            ("can_delete_hostuser", ("可以删除服务器用户信息")),
            ("can_view_hostuser", ("可以查看服务器用户信息")),
        )

class HostGroup(models.Model):
    name = models.CharField(max_length=32,unique=True,verbose_name=u'组名')
    servers = models.ManyToManyField('Assets')
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'hostgroups'
        verbose_name = u'主机组'
        verbose_name_plural = u'主机组'
        permissions = (
            ("can_add_hostgroup", ("可以添加主机组")),
            ("can_change_hostgroup", ("可以修改主机组信息")),
            ("can_delete_hostrgroup", ("可以删除主机组")),
            ("can_view_hostgroup", ("可以查看主机组")),
        )