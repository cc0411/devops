# -*- coding: utf-8 -*-
from django.db import models
from index.models import UserProfile
from asset.models import Assets,HostGroup
import  uuid
from django.core.exceptions import ValidationError
try:
    import simplejson as json
except ImportError:
    import json
# Create your models here.
class Audit(models.Model):
    server = models.ForeignKey(Assets)
    channel = models.CharField(max_length=100,verbose_name='Channel name',blank=False,unique=True,editable=False)
    log = models.UUIDField(max_length=100,default=uuid.uuid4,verbose_name='Log name',blank=False,unique=True,editable=False)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_created=True,auto_now=True)
    is_finished = models.BooleanField(default=False)
    user = models.ForeignKey(UserProfile)
    width = models.PositiveIntegerField(default=90)
    height = models.PositiveIntegerField(default=40)
    def __unicode__(self):
        return '%s-%s' %(self.server.hostname,self.server.wip)

    class Meta:
        db_table = 'audit'
        verbose_name = u'操作日志'
        verbose_name_plural = u'操作日志'
        permissions = (
            ("can_delete_audit", ("可以删除操作日志")),
            ("can_view_audit", ("可以查看操作日志")),
            ("can_play_audit", ("可以播放操作日志")),
        )
