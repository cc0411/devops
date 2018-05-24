本系统基于python2.7.10+centos7.2系统开发，目前已实现了webshell，cmdb，批量任务和批量文件管理，请大家star
使用方法
1.请先安装模块
pip install -r requirements.txt
2.数据库初始化，目前使用sqllite，有需要的可以更改setting修改为mysql
python manage.py  makemigrations
python manage.py migrate
3.创建系统管理员账户
python manage.py createsuperuser
4.启动
python manage.py  runserver 0.0.0.0:8000

系统使用说明
一.资产管理实现以下几个功能
1.资产查看，修改与添加
![image](https://github.com/cc0411/devops/tree/master/snapshot/资产查看.png)
![image](https://github.com/cc0411/devops/tree/master/snapshot/资产添加.png)
2.主机账户查看，修改与添加
3.机房查看，修改与添加
![image](https://github.com/cc0411/devops/tree/master/snapshot/机房查看.png)
![image](https://github.com/cc0411/devops/tree/master/snapshot/机房添加.png)
4.主机组查看，修改与添加
5.资产导出
二.跳板机实现以下几个功能
1.主机连接
注使用此功能前，需要登陆后台,用户信息添加需要授权的主机组
![image](https://github.com/cc0411/devops/tree/master/snapshot/终端连接1.png)
![image](https://github.com/cc0411/devops/tree/master/snapshot/终端连接2.png)
2.日志审计
![image](https://github.com/cc0411/devops/tree/master/snapshot/终端审计.png)
![image](https://github.com/cc0411/devops/tree/master/snapshot/日志审计2.png)
三.自动化实现以下几个功能,使用以下功能时需要在后台用户信息处添加该用户授权的主机和主机组
1.批量命令
![image](https://github.com/cc0411/devops/tree/master/snapshot/批量命令.png)
2.批量文件传输
![image](https://github.com/cc0411/devops/tree/master/snapshot/批量文件传输.png)
3.批量任务的日志审计
![image](https://github.com/cc0411/devops/tree/master/snapshot/批量任务审计.png)
四.登陆日志审计
![image](https://github.com/cc0411/devops/tree/master/snapshot/登陆审计.png)
五.后台管理
![image](https://github.com/cc0411/devops/tree/master/snapshot/后台管理.png)
六.API
![image](https://github.com/cc0411/devops/tree/master/snapshot/api.png)
七.权限管理
打开后台添加一个账户，添加授权主机，主机组和权限
![image](https://github.com/cc0411/devops/tree/master/snapshot/权限审计.png)
如果该用户没有权限，打开页面时会提示403
![image](https://github.com/cc0411/devops/tree/master/snapshot/权限审计2.png)
