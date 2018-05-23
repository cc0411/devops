# -*- coding:utf-8 -*-
import sys,os,json
import paramiko
from  concurrent.futures import ThreadPoolExecutor

def  ssh_cmd(sub_task_obj):
    host = sub_task_obj.host
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host.wip,
        port = host.ssh_port,
        username = host.user.username,
        password = host.user.password,
        timeout=5)
        stdin,stdout,stderr = ssh.exec_command(sub_task_obj.task.content)
        stdout_res = stdout.read()
        stderr_res = stderr.read()
        sub_task_obj.result = stdout_res + stderr_res
        print(sub_task_obj.result)
        if stderr_res:
            sub_task_obj.status =2
        else:
            sub_task_obj.status =1
    except Exception as e:
        sub_task_obj.result =e
        sub_task_obj.status =2
    sub_task_obj.save()
    ssh.close()


def  file_transfer(sub_task_obj,task_data):
    host = sub_task_obj.host
    try:
        t = paramiko.Transport(host.wip,host.port)
        t.connect(username = host.user.username,password=host.user.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if task_data['file_transfer_type'] =='send':
            sftp.put(task_data["local_file_path"], task_data["remote_file_path"])
            result = "file sends successd"
        else:
            local_file_path = conf.settings.DOWNLOAD_DIR
            if  not os.path.isdir("%s%s" %(local_file_path,task_obj.id)):
                os.mkdir("%s%s" %local_file_path,task_obj.id)
            filename = "%s.%s" %(host.wip,task_data["remote_file_path"].split('/')[-1])
            sftp.get(task_data["remote_file_path"], "%s%s/%s"% (local_file_path,sub_task_obj.task.id, filename))
            result = "download remote file [%s] succeed!"  % task_data["remote_file_path"]
        t.close()
        sub_task_obj.status =1
    except Exception as e:
        result = e
        sub_task_obj.status =2

    sub_task_obj.result = result
    sub_task_obj.save()

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devops.settings")
    import django
    django.setup()
    from django import conf
    from tasks import models
    if len(sys.argv) == 1:
        exit("task id not provided!")
    task_id = sys.argv[1]
    task_obj = models.Task.objects.get(id=task_id)
    print("task runner..",task_obj)
    pool = ThreadPoolExecutor(10)
    if task_obj.task_type == 'cmd':
        for sub_task_obj in task_obj.tasklogdetail_set.all():
           pool.submit(ssh_cmd,sub_task_obj)
    else: #文件传输
        task_data = json.loads(task_obj.content)
        for sub_task_obj in task_obj.tasklogdetail_set.all():
            pool.submit(file_transfer,sub_task_obj,task_data )
    pool.shutdown(wait=True)
