# -*- coding: utf-8 -*-
from django.db import models
from index.models import UserProfile
from asset.models import Assets
from django_celery_results.models import TaskResult
from jsonfield import JSONField
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


class Tools(models.Model):
    TOOL_RUN_TYPE = (
        ('shell', 'shell'),
        ('python', 'python'),
        ('yml', 'yml'),
    )

    name = models.CharField(max_length=255, verbose_name='工具名称', unique=True)
    tool_script = models.TextField(verbose_name='脚本内容', null=True, blank=True)
    tool_run_type = models.CharField(choices=TOOL_RUN_TYPE, verbose_name='脚本类型', max_length=24)
    comment = models.TextField(verbose_name='工具说明', null=True, blank=True)

    ctime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    utime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "Tools"
        verbose_name = "工具"
        verbose_name_plural = verbose_name
        permissions ={
            ("can_add_tools", ("可以添加工具")),
            ("can_change_tools", ("可以修改工具信息")),
            ("can_delete_tools", ("可以删除工具")),
            ("can_view_tools", ("可以查看工具信息")),

        }



class ToolsResults(models.Model):
    task_id = models.UUIDField(max_length=255, verbose_name='任务ID', unique=True)
    add_user = models.CharField(max_length=255, verbose_name='创建者', null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @property
    def status(self):
        status = TaskResult.objects.get(task_id=self.task_id).status
        return status

    class Meta:
        db_table = "ToolsResults"
        verbose_name = "任务结果"
        verbose_name_plural = verbose_name
        permissions ={
            ("can_view_toolsresult", ("可以查看任务结果")),

        }



class Variable(models.Model):
    name = models.CharField(max_length=200, verbose_name='变量组名字')
    desc = models.TextField(null=True, blank=True, verbose_name='描述')
    vars = JSONField(null=True, blank=True, default={}, verbose_name='变量')
    assets = models.ManyToManyField(Assets, verbose_name='关联资产', related_name='asset', blank=True)

    ctime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    utime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "Variable"
        verbose_name = "变量组"
        verbose_name_plural = verbose_name
        permissions ={
            ("can_add_var", ("可以添加变量")),
            ("can_change_var", ("可以修改变量信息")),
            ("can_delete_var", ("可以删除变量")),
            ("can_view_var", ("可以查看变量信息")),

        }