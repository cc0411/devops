# -*- coding: utf-8 -*-
from django.contrib import admin
from tasks import  models
# Register your models here.

admin.site.register(models.Task)
admin.site.register(models.TaskLogDetail)
