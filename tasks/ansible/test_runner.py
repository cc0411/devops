# -*- coding:utf-8 -*-

import sys
sys.path.insert(0,"../..")
import json
from tasks.ansible.runner import AdHocRunner,CommandRunner,PlayBookRunner
from tasks.ansible.inventory import BaseInventory




def  TestAdHocRunner():
        """
         以yml的形式 执行多个命令
        :return:
        """

        host_data = [
            {
                "hostname": "192.168.10.102",
                "ip": "192.168.10.102",
                "port": 22,
                "username": "root",
                "password": "123456",
            },
        ]
        inventory = BaseInventory(host_data)
        runner = AdHocRunner(inventory)

        tasks = [
            #{"action": {"module": "cron","args": "name=\"sync time\" minute=\"*/3\" job=\"/usr/sbin/ntpdate time.nist.gov &> /dev/null\"" }, "name": "run_cmd"},
            {"action": {"module": "shell", "args": "ifconfig"}, "name": "run_whoami"},
        ]
        ret = runner.run(tasks, "all")
        print(ret.results_summary)
        print(ret.results_raw)

def TestCommandRunner():
        """
        执行单个命令，返回结果
        :return:
        """

        host_data = [
            {
                "hostname": "192.168.10.102",
                "ip": "192.168.10.102",
                "port": 22,
                "username": "root",
                "password": "123456",
            },
        ]
        inventory = BaseInventory(host_data)
        runner = CommandRunner(inventory)

        #该模块可以运行command，shell，raw，script，直接写入参数即可。
        res = runner.execute('df -h', 'all')
        #res = runner.execute("/root/sayhell.sh", 'all')
        #print(res.results_command)
        res_command = res.results_command
        print('------------')
        print(json.dumps(res_command))

        #print(res.results_raw)
        print('-------------')
        print(json.dumps(res.results_raw))
        #print(res.results_command['10.135.133.214']['stdout'])

if __name__ == "__main__":
    #TestAdHocRunner()
    TestCommandRunner()