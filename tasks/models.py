# -*- coding: utf-8 -*-
from django.db import models
from index.models import UserProfile
from asset.models import Assets
# Create your models here.

class Task(models.Model):
    """批量任务"""
    task_type_choices = (('cmd','批量命令'),('file-transfer','文件传输'))
    task_type = models.CharField(choices=task_type_choices,max_length=64)
    content = models.CharField(max_length=255, verbose_name="任务内容")
    user = models.ForeignKey(UserProfile)

    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s"%(self.task_type,self.content)

    class Meta:
        db_table = 'task'
        verbose_name_plural = u'Task'
        verbose_name = u'Task'
        permissions = (
            ("can_delete_task", ("可以删除task")),
            ("can_view_task", ("可以查看task")),
        )

class TaskLogDetail(models.Model):
    """存储大任务子结果"""
    task = models.ForeignKey("Task")
    host = models.ForeignKey(Assets)
    result = models.TextField(verbose_name="任务执行结果")

    status_choices = ((0,'initialized'),(1,'sucess'),(2,'failed'),(3,'timeout'))
    status = models.SmallIntegerField(choices=status_choices,default=0)

    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s"%(self.task,self.host)

    class Meta:
        db_table = 'tasklogdetail'
        verbose_name_plural = u'Tasklogdetail'
        verbose_name = u'Tasklogdetail'
        permissions = (
            ("can_delete_session", ("可以删除tasklog")),
            ("can_view_session", ("可以查看tasklog")),
        )
