# -*- coding: utf-8 -*-
from django.contrib import admin
from asset import  models
# Register your models here.



admin.site.register(models.Assets)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUsers)
admin.site.register(models.IDC)
