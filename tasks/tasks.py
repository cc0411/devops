#-*- coding:utf-8 -*-
from __future__ import absolute_import
from  multiprocessing import  current_process
from asset.models import Assets
from .ansible.runner import AdHocRunner,PlayBookRunner
from .ansible.inventory import BaseInventory
from  celery import shared_task
import  random
import os
from . import  models



@shared_task()
def ansbile_tools(assets, tasks):
    current_process()._config = {'semprefix': '/mp'}

    inventory = BaseInventory(host_list=assets)
    hostname, retsult_data = [], []
    ret = None
    for i in assets:
        hostname.append(i['hostname'])

    for t in tasks:
        if t['action']['module'] == "script":
            runner = AdHocRunner(inventory)
            t1 = [t]
            retsult = runner.run(t1, "all")
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
                ret =("{}".format(e))

            for i in range(len(hostname)):
                std, ret_host = [], {}
                try:
                    out = ret[hostname[i]][t['name']]['stdout']
                    if not out:
                        out = ret[hostname[i]][t['name']]['stderr']
                    std.append("{0}".format(out))
                except Exception as e:
                    ret=e
                    try:
                        std.append("{0}".format(ret[hostname[i]][t['name']]['msg']))
                    except Exception as e:
                        ret = ("{0}执行失败{1}".format(t['name'], e))
                ret_host['hostname'] = hostname[i]
                ret_host['data'] = ''.join(std)
                retsult_data.append(ret_host)

        elif t['action']['module'] == 'yml':
            runers = PlayBookRunner(playbook_path=t['action']['args'], inventory=inventory)
            retsult = runers.run()
            try:
                ret = retsult['results_callback']
            except Exception as e:
                ret=e

            for i in range(len(hostname)):
                std, ret_host = [], {}
                try:
                    out = ret[hostname[i]]['stdout']
                    if not out:
                        out = ret[hostname[i]]['stderr']
                    std.append("{0}".format(out))
                except Exception as e:
                    ret =e
                    try:
                        std.append("{0}".format(ret[hostname[i]]['msg']))
                    except Exception as e:
                        ret =("{0}执行失败".format(e))
                ret_host['hostname'] = hostname[i]
                ret_host['data'] = ''.join(std)
                retsult_data.append(ret_host)

    return retsult_data

@shared_task
def ansbile_asset_hardware(ids, assets):
    current_process()._config = {'semprefix': '/mp'}

    inventory = BaseInventory(host_list=assets)
    runner = AdHocRunner(inventory)
    tasks = [
        {"action": {"module": "setup", "args": ""}, "name": "script"},
    ]
    retsult = runner.run(tasks, "all")
    hostname = assets[0]['hostname']

    try:
        data = retsult.results_raw['ok'][hostname]['script']['ansible_facts']
        disk = "{}".format(str(sum([int(data["ansible_devices"][i]["sectors"]) *
                                    int(data["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024
                                    for i in data["ansible_devices"] if
                                    i[0:2] in ("vd", "ss", "sd")])) + str(" GB"))
        memory = round(data['ansible_memtotal_mb'] / 1024)
        cpu = int("{}".format(data['ansible_processor_count'] * data["ansible_processor_cores"]))

        system_type = data['ansible_product_name'] + "" + data['ansible_lsb']["description"]
        Assets.objects.filter(id=ids).update(hostname=hostname,
                                                disk=disk,
                                                memory=memory,
                                                cpu=cpu,
                                                system_type=system_type)
    except Exception as e:
        return "获取资产信息 {0} 失败 {1}".format(hostname,e)
    return "获取资产信息 {} 成功".format(hostname)

@shared_task
def ansbile_tools_crontab(tools_name, *args):
    current_process()._config = {'semprefix': '/mp'}

    a_list, assets_list = [], []
    for i in args:
        Assets.objects.get(hostname=i)
        a_list.append(Assets.objects.get(hostname=i))

    t_obj = models.Tools.objects.get(name=tools_name)

    for i in a_list:
        var_all = {
            'hostname': i.hostname,
            'lip': i.lip,
            "wip": i.wip,
        }
        try:
            var_all.update(models.Variable.objects.get(assets__hostname=i.hostname).vars)
        except Exception as e:
            pass

        assets_list.append({
            "hostname": i.hostname,
            "ip": i.lip,
            "port": i.ssh_port,
            "username": i.user.username,
            "password": i.user.password,
            "private_key": i.user.key,
            "vars": var_all,
        }, )

    file = "data/script/{0}".format(random.randint(0, 999999))
    file2 = "data/script/{0}".format(random.randint(1000000, 9999999))

    tools, modules = None, None
    if t_obj.tool_run_type == 'shell' or t_obj.tool_run_type == 'python':
        with open("{}.sh".format(file), 'w+') as f:
            f.write(t_obj.tool_script)
        os.system(
            "sed  's/\r//'  {0}.sh >  {1}.sh".format(file, file2))
        tools = '{}.sh'.format(file2)
        modules = "script"
    elif t_obj.tool_run_type == 'yml':

        with open("{}.yml".format(file), 'w+') as f:
            f.write(t_obj.tool_script)
        os.system("sed  's/\r//'  {0}.yml >  {1}.yml".format(file, file2))
        tools = '{}.yml'.format(file2)
        modules = "yml"

    inventory = BaseInventory(host_list=assets_list)
    hostname, retsult_data = [], []

    for i in inventory.hosts:
        hostname.append(i)
    ret = None

    if modules == "script":
        runner = AdHocRunner(inventory)
        tasks = [{"action": {"module": "{}".format(modules), "args": "{}".format(tools)}, "name": "script"}, ]
        retsult = runner.run(tasks, "all")

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
            ret =e

        for i, element in enumerate(hostname):
            std, ret_host = [], {}
            try:
                out = ret[element]['script']['stdout']
                if not out:
                    out = ret[element]['script']['stderr']
                std.append("{0}".format(out))
            except Exception as e:
                print(e)
                try:
                    std.append("{0}".format(ret[element]['script']['msg']))
                except Exception as e:
                    print("执行失败{0}".format(e))
            ret_host['hostname'] = element
            ret_host['data'] = ''.join(std)
            retsult_data.append(ret_host)

    elif modules == 'yml':
        runers = PlayBookRunner(playbook_path=tools, inventory=inventory)
        retsult = runers.run()

        try:
            ret = retsult['results_callback']
        except Exception as e:
            print("{}".format(e))
        for i, element in enumerate(hostname):
            std, ret_host = [], {}
            try:
                out = ret[element]['stdout']
                if not out:
                    out = ret[element]['stderr']
                std.append("{0}".format(out))
            except Exception as e:
                print(e)
                try:
                    std.append("{0}".format(ret[element]['msg']))
                except Exception as e:
                    print("执行失败{0}".format(e))
            ret_host['hostname'] = element
            ret_host['data'] = ''.join(std)
            retsult_data.append(ret_host)
    return retsult_data


























