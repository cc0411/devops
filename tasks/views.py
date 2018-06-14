# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import  login_required
from django.http import  HttpResponse
from .utils.multitask import MultiTaskManger
from . import  models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView,CreateView,View,UpdateView,DetailView
from asset.models import Assets
from . import  forms
from .models import Tools,Variable,ToolsResults
from .ansible.inventory import BaseInventory
from .ansible.runner import AdHocRunner
from django_celery_results.models import TaskResult
from django.urls import reverse_lazy
import  os,random,time
from .tasks import ansbile_tools
# Create your views here.

cmd_list = [
    'shell',
    'file',
    'yum',

]



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



class TasksCmd(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    """
    任务cmd 界面
    """
    template_name = 'ansible/cmd.html'
    model = Assets
    context_object_name = "asset_list"
    queryset = Assets.objects.all()
    ordering = ('-id',)
    permission_required = ''
    raise_exception = True

    def get_context_data(self,object_list=None, **kwargs):
        context = {
            "cmd_list": cmd_list,
        }
        kwargs.update(context)
        return super(TasksCmd,self).get_context_data(**kwargs)

def cmdjob(assets, tasks):
    """
    :param assets:  资产帐号密码
    :param tasks:  执行的命令 和 模块
    :return:  执行结果
    """

    inventory = BaseInventory(host_list=assets)
    hostname = []
    for i in inventory.hosts:
        hostname.append(i)
    runner = AdHocRunner(inventory)
    retsult = runner.run(tasks, "all")
    ret = None
    try:
        ok = retsult.results_raw['ok']
        failed = retsult.results_raw['failed']
        unreachable = retsult.results_raw['unreachable']
        if not ok and not failed:
            ret = unreachable
        elif not ok:
            ret = failed
        else:
            ret = ok
    except Exception as e:
        print(e)

    retsult_data = []

    for i, element in enumerate(hostname):
        std, ret_host = [], {}
        for t in range(len(tasks)):
            try:
                out = ret[element]['task{}'.format(t)]['stdout']
                err = ret[element]['task{}'.format(t)]['stderr']
                std.append("{0}{1}".format(out, err))
            except Exception as e:
                print(e)
                try:
                    std.append("{0} \n".format(
                        ret[hostname[i]]['task{}'.format(t)]['msg'], t + 1))
                except Exception as e:
                    print("第{0}个执行失败,此任务后面的任务未执行 {1}".format(t + 1, e))
                    std.append("第{0}个执行失败,此任务后面的任务未执行".format(t + 1))

        ret_host['hostname'] = element
        ret_host['data'] = '\n'.join(std)
        retsult_data.append(ret_host)

    return retsult_data

class TasksPerform(LoginRequiredMixin, View):
    """
    执行 cmd  命令
    """

    @staticmethod
    def post(request):
        ids = request.POST.getlist('id')
        args = request.POST.getlist('args', None)
        modules = request.POST.getlist('module', None)
        ret_data = {'data': []}
        if not ids or args == [''] or not modules:
            ret = {'hostname': None, 'data': "请选中服务器,输入要执行的命令"}
            ret_data['data'].append(ret)
            return HttpResponse(json.dumps(ret_data))

        idstring = ','.join(ids)
        asset_obj = Assets.objects.extra(where=['id IN (' + idstring + ')'])

        for i in asset_obj:
            project = Assets.objects.get(hostname=i).project
        tasks, assets = [], []
        for x in range(len(modules)):
            tasks.append(
                {"action": {"module": modules[x], "args": args[x]}, "name": 'task{}'.format(x)}, )

            assets.append({
                "hostname": i.hostname,
                "ip": i.lip,
                "port": i.ssh_port,
                "username": i.user.username,
                "password": i.user.password,
                "private_key": i.user.key,

            }, )
        t = cmdjob(assets, tasks)
        ret_data['data'] = t
        return HttpResponse(json.dumps(ret_data))

class ToolsList(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    """
    工具列表
    """
    template_name = 'ansible/tools.html'
    model = Tools
    context_object_name = "tools_list"
    queryset = Tools.objects.all()
    ordering = ('-id',)
    permission_required = 'tasks.can_view_tools',
    raise_exception = True

class ToolsAdd(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    """
     工具增加
    """
    model = Tools
    form_class = forms.ToolsForm
    template_name = 'ansible/tools-add-update.html'
    success_url = reverse_lazy('toolslist')
    permission_required = 'tasks.can_add_tools'
    raise_exception = True

class ToolsUpdate(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    """
     工具更新
    """
    model = Tools
    form_class = forms.ToolsForm
    template_name = 'ansible/tools-add-update.html'
    success_url = reverse_lazy('toolslist')

    permission_required = 'tasks.can_change_tools'
    raise_exception = True

    def form_invalid(self, form):
        return super(ToolsUpdate, self).form_invalid(form)

class ToolsAllDel(LoginRequiredMixin, PermissionRequiredMixin,View):
    """
    工具删除
    """
    model = Tools
    permission_required = 'tasks.can_delete_tools'
    raise_exception = True
    @staticmethod
    def post(request):
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('nid'):
                ids = request.POST.get('nid', None)
                Tools.objects.get(id=ids).delete()
            else:
                ids = request.POST.getlist('id', None)
                idstring = ','.join(ids)
                Tools.objects.extra(
                    where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,没有权限{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))

class ToolsExec(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    """
    工具执行
    """
    template_name = 'ansible/tools-exec.html'
    model = Assets
    context_object_name = "asset_list"
    queryset = Assets.objects.all()
    ordering = ('-id',)

    def get_context_data(self,  object_list=None, **kwargs):
        tools_list = Tools.objects.all()
        context = {
            "tools_list": tools_list
        }
        kwargs.update(context)
        return super(ToolsExec,self).get_context_data(**kwargs)
    @staticmethod
    def post(request):
        """
        执行工具
        :param request:  asset_id,tool_id,priority
        :return:  ret
        """
        ret = {'status': True, 'error': None, }
        try:
            asset_id = request.POST.getlist('asset_id', None)
            tool_id = request.POST.getlist('tool_id', None)
            priority = request.POST.getlist('priority', None)
            if asset_id == [] or tool_id == [] or priority == ['']:
                ret['status'] = False
                ret['error'] = '未选择主机 或 未选择脚本 或 未设置优先级'
                return HttpResponse(json.dumps(ret))

            for i in priority:
                if priority.count(i) >= 2:
                    ret['status'] = False
                    ret['error'] = '优先级设置有重复 ,请重新修改！！！'
                    return HttpResponse(json.dumps(ret))

            asset_id_tring = ','.join(asset_id)
            asset_obj = Assets.objects.extra(where=['id IN (' + asset_id_tring + ')'])

            assets = []
            for i in asset_obj:
                var_all = {
                    'hostname': i.hostname,
                    'lip': i.lip,
                    "wip": i.wip,

                }
                try:
                    var_all.update(Variable.objects.get(assets__hostname=i).vars)
                except Exception as e:
                    pass

                assets.append({
                    "hostname": i.hostname,
                    "ip": i.lip,
                    "port": i.ssh_port,
                    "username": i.user.username,
                    "password": i.user.password,
                    "private_key": i.user.key,
                    "vars": var_all,
                }, )

            tool_priority_1 = dict(zip(tool_id, priority))
            tool_priority = sorted(tool_priority_1.items(), key=lambda item: item[1])

            tasks = []
            for i in tool_priority:
                tool_obj = Tools.objects.get(id=i[0])
                if tool_obj.tool_run_type == 'shell' or tool_obj.tool_run_type == 'python':
                    t = time.time()
                    file = "data/script/{0}".format(int(round(t * 1000)) + random.randint(0, 999999))
                    t1 = time.time()
                    file2 = "data/script/{0}".format(int(round(t1 * 1000)) + random.randint(10000000, 99999999))
                    with open("{}.sh".format(file), 'w+') as f:
                        f.write(tool_obj.tool_script)
                    os.system("sed  's/\r//'  {0}.sh >  {1}.sh".format(file, file2))
                    tasks.append({"action": {"module": "script", "args": '{}.sh'.format(file2), },
                                  "name": 'task{}'.format(i[1])}, )

                elif tool_obj.tool_run_type == 'yml':
                    t = time.time()
                    file = "data/script/{0}".format(int(round(t * 1000)) + random.randint(0, 999999))
                    t1 = time.time()
                    file2 = "data/script/{0}".format(int(round(t1 * 1000)) + random.randint(10000000, 99999999))
                    with open("{}.yml".format(file), 'w+') as f:
                        f.write(tool_obj.tool_script)
                    os.system("sed  's/\r//'  {0}.yml >  {1}.yml".format(file, file2))
                    tasks.append({"action": {"module": "yml", "args": '{}.yml'.format(file2), },
                                  "name": 'task{}'.format(i[1])}, )

            rets = ansbile_tools.delay(assets, tasks)
            task_obj = ToolsResults.objects.create(task_id=rets.task_id)
            ret['id'] = task_obj.id
            return HttpResponse(json.dumps(ret))
        except Exception as e:
            ret['status'] = False
            ret['error'] = '创建任务失败,{0}'.format(e)
            return HttpResponse(json.dumps(ret))

class ToolsResultsList(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    """
    执行工具 返回信息列表
    """
    ordering = ('-ctime',)
    template_name = 'tasks/tools-results.html'
    model = ToolsResults
    queryset = models.ToolsResults.objects.all()
    permission_required = 'tasks.can_view_toolsresult',
    raise_exception = True

class ToolsResultsDetail(LoginRequiredMixin, PermissionRequiredMixin,DetailView):
    """
     执行工具 结果详细
    """

    model = models.ToolsResults
    template_name = 'tasks/tools-results-detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        task = models.ToolsResults.objects.get(id=pk)
        try:
            results = TaskResult.objects.get(task_id=task.task_id)
        except Exception as e:
            results = {'result': "还未完成,请稍后再查看！！"}

        context = {
            "task": task,
            "results": results,
        }
        kwargs.update(context)
        return super(ToolsResultsDetail,self).get_context_data(**kwargs)

class VarsList(LoginRequiredMixin, ListView,PermissionRequiredMixin):
    """
    Vars变量 列表
    """
    template_name = 'ansible/vars.html'
    model = Variable
    context_object_name = "vars_list"
    ordering = ('-id',)
    queryset = models.Variable.objects.all()
    permission_required = 'tasks.can_view_var',
    raise_exception = True

class VarsAdd(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    """
     Vars变量 增加
    """
    model = Variable
    form_class = forms.VarsForm
    template_name = 'ansible/vars-add-update.html'
    success_url = reverse_lazy('varlist')
    permission_required = 'tasks.can_add_var'
    raise_exception = True

class VarsUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    """
    Vars变量 更新
    """
    model = Variable
    form_class = forms.VarsForm
    template_name = 'ansible/vars-add-update.html'
    success_url = reverse_lazy('varlist')
    permission_required = 'tasks.can_change_var'
    raise_exception = True

    def form_invalid(self, form):
        return super(VarsUpdate, self).form_invalid(form)

class VarsAllDel(LoginRequiredMixin, PermissionRequiredMixin,View):
    """
    工具删除
    """
    model = Variable
    permission_required = 'tasks.can_delete_var'
    raise_exception = True

    @staticmethod
    def post(request):
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('nid'):
                ids = request.POST.get('nid', None)
                Variable.objects.get(id=ids).delete()
            else:
                ids = request.POST.getlist('id', None)
                idstring = ','.join(ids)
                Variable.objects.extra(where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,没有权限{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))

