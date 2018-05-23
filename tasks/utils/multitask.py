# -*- coding:utf-8 -*-

import json,subprocess
from django import  conf
from tasks import  models


class MultiTaskManger(object):
    def __init__(self,request):
        self.request = request
        self.run_task()
    def task_parser(self):
        '''
        解析任务
        '''
        self.task_data = json.loads(self.request.POST.get('task_data'))
        task_type = self.task_data.get('task_type')
        if hasattr(self,task_type):
            task_func = getattr(self,task_type)
            task_func()
        else:
            print("not found task",task_type)
    def run_task(self):
        '''
        调用任务
        '''
        self.task_parser()


    def  cmd(self):
        task_obj = models.Task.objects.create(task_type = 'cmd',content=self.task_data.get('cmd'),user=self.request.user)
        seleted_host_ids = set(self.task_data['selected_hosts'])

        task_log_objs = []
        for id  in seleted_host_ids:
            task_log_objs.append(models.TaskLogDetail(task=task_obj,host_id=id,result='init......'))
        models.TaskLogDetail.objects.bulk_create(task_log_objs)

        task_script ="python %s/tasks/utils/task_runner.py  %s"  %(conf.settings.BASE_DIR,task_obj.id)
        cmd_process = subprocess.Popen(task_script,shell=True)
        print("runing batch commands")
        self.task_obj = task_obj

    def  file_transfer(self):
        '''
        文件分发
        '''
        task_obj = models.Task.objects.create(task_type = 'file_transfer',content = json.dumps(self.task_data),user=self.request.user)
        selected_host_ids = set(self.task_data['selected_hosts'])
        task_log_objs = []
        for id in selected_host_ids:
            task_log_objs.append(models.TaskLogDetail(task=task_obj,host_id=id,result='init....')
                                 )
        models.TaskLogDetail.objects.bulk_create(task_log_objs)
        task_script = 'python %s/tasks/utils/task_runner.py %s' %(conf.settings.BASE_DIR,task_obj.id)

        cmd_process = subprocess.Popen(task_script,shell=True)
        print("running  batch  file  transfer")

        self.task_obj = task_obj