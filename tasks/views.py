# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import  login_required
from django.http import  JsonResponse
from asset import  models
from django.http import  HttpResponse
from django.core import  serializers
from tasks.utils.multitask import MultiTaskManger
from tasks import  models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView
# Create your views here.




@login_required()
def host_mgr(request):
    return  render(request,'ansible/host_mgr.html')


@login_required()
def  file_transfer(request):
    return  render(request,'ansible/file_transfer.html')

import json

@login_required()
def  batch_task_mgr(request):
    task_data =json.loads(request.POST.get('task_data'))
    task_obj = MultiTaskManger(request)
    print(task_obj.task_obj.id)
    response = {
        'task_id': task_obj.task_obj.id,
        'selected_hosts':list(task_obj.task_obj.tasklogdetail_set.all().values('id','host__wip','host__hostname','host__user__username'))
    }
    return  HttpResponse(json.dumps(response))
def task_result(request):
    task_id = request.GET.get('task_id')
    sub_tasklog_objs = models.TaskLogDetail.objects.filter(task_id=task_id)
    log_data = list(sub_tasklog_objs.values('id','status','result'))
    return HttpResponse(json.dumps(log_data))

class TasklogList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    template_name = 'ansible/tasklog.html'
    model = models.TaskLogDetail
    context_object_name =  "tasklog_list"
    queryset = models.TaskLogDetail.objects.all()
    ordering = ('-id'),
    permission_required = 'task.can_view_session'
    raise_exception = True