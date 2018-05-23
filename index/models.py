# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import django
from asset.models import HostGroup,Assets
from index import auth

# Create your models here.

class UserProfile(auth.AbstractBaseUser,auth.PermissionsMixin):
    email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
    )
    is_active = models.BooleanField(default=True)
    objects = auth.UserManager()
    name = models.CharField(max_length=32)
    host_groups = models.ManyToManyField(HostGroup, verbose_name='授权主机组', blank=True)
    bind_hosts = models.ManyToManyField(Assets, verbose_name='授权主机', blank=True)
    memo = models.TextField('备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    valid_begin_time = models.DateTimeField(default=django.utils.timezone.now, help_text="yyyy-mm-dd HH:MM:SS")
    valid_end_time = models.DateTimeField(blank=True, null=True, help_text="yyyy-mm-dd HH:MM:SS")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    def get_full_name(self):
        # The user is identified by their email address
        return self.email
    def get_short_name(self):
        # The user is identified by their email address
        return self.email
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_active
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'userprofile'
        verbose_name = '用户信息'
        verbose_name_plural = u"用户信息"


class Loginlog(models.Model):
    user = models.CharField(max_length=32)
    ip = models.GenericIPAddressField()
    action = models.CharField(max_length=32)
    ctime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'loginlog'
        verbose_name_plural = u'Loginlog'
        verbose_name = u'Loginlog'
        permissions =(
            ("can_delete_loginlog", ("可以删除登录日志")),
            ("can_view_loginlog", ("可以查看登录日志")),
        )
