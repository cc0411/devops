#-*- coding:utf-8 -*-
import paramiko
import socket
from channels.generic.websockets import WebsocketConsumer
try:
    import simplejson as json
except ImportError:
    import json
from devops.interactive import interactive_shell,get_redis_instance,SshTerminalThread,InterActiveShellThread
import sys
from django.utils.encoding import smart_unicode
from django.core.exceptions import ObjectDoesNotExist
from asset.models import Assets,HostGroup
from jump.models import Audit
from index.models import UserProfile
from devops.sudoterminal import ShellHandlerThread
import ast
import time
from django.utils.timezone import now
import os
from channels import Group

class webterminal(WebsocketConsumer):

    ssh = paramiko.SSHClient()
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True


    def connect(self, message):
        self.message.reply_channel.send({"accept": True})
        #permission auth
        self.message.reply_channel.send({"text":json.dumps(['channel_name',self.message.reply_channel.name])},immediately=True)

    def disconnect(self, message):
        #close threading
        self.closessh()

        self.message.reply_channel.send({"accept":False})

        audit_log=Audit.objects.get(user=UserProfile.objects.get(email=self.message.user),channel=self.message.reply_channel.name)
        audit_log.is_finished = True
        audit_log.end_time = now()
        audit_log.save()
        self.close()

    def queue(self):
        queue = get_redis_instance()
        channel = queue.pubsub()
        return queue

    def closessh(self):
        #close threading
        self.queue().publish(self.message.reply_channel.name, json.dumps(['close']))

    def receive(self,text=None, bytes=None, **kwargs):
        try:
            if text:
                data = json.loads(text)
                begin_time = time.time()
                if data[0] == 'ip':
                    ip = data[1]
                    width = data[2]
                    height = data[3]
                    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        data = Assets.objects.get(wip=ip)
                        port = data.ssh_port
                        method = data.user.auth_method
                        username = data.user.username
                        audit_log = Audit.objects.create(user=UserProfile.objects.get(email=self.message.user),server=data,channel=self.message.reply_channel.name,width=width,height=height)
                        audit_log.save()
                        if method == 'ssh-password':
                            password = data.user.password
                        else:
                            key = data.user.key
                    except ObjectDoesNotExist:
                        self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31mConnect to server! Server ip doesn\'t exist!\033[0m'])},immediately=True)
                        self.message.reply_channel.send({"accept":False})
                    try:
                        if method == 'ssh-password':
                            self.ssh.connect(ip, port=port, username=username, password=password, timeout=3)
                        else:
                            self.ssh.connect(ip, port=port, username=username, key_filename=key, timeout=3)
                    except socket.timeout:
                        self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31mConnect to server time out\033[0m'])},immediately=True)
                        self.message.reply_channel.send({"accept":False})
                        return
                    except Exception:
                        self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31mCan not connect to server\033[0m'])},immediately=True)
                        self.message.reply_channel.send({"accept":False})
                        return

                    chan = self.ssh.invoke_shell(width=width, height=height,)

                    #open a new threading to handle ssh to avoid global variable bug
                    sshterminal=SshTerminalThread(self.message,chan)
                    sshterminal.setDaemon = True
                    sshterminal.start()

                    directory_date_time = now()
                    log_name = os.path.join('{0}-{1}-{2}'.format(directory_date_time.year,directory_date_time.month,directory_date_time.day),'{0}.json'.format(audit_log.log))

                    #interactive_shell(chan,self.message.reply_channel.name,log_name=log_name,width=width,height=height)
                    interactivessh = InterActiveShellThread(chan,self.message.reply_channel.name,log_name=log_name,width=width,height=height)
                    interactivessh.setDaemon = True
                    interactivessh.start()

                elif data[0] in ['stdin','stdout']:
                    self.queue().publish(self.message.reply_channel.name, json.loads(text)[1])
                elif data[0] == u'set_size':
                    self.queue().publish(self.message.reply_channel.name, text)
                else:
                    self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31mUnknow command found!\033[0m'])},immediately=True)
            elif bytes:
                self.queue().publish(self.message.reply_channel.name, json.loads(bytes)[1])
        except socket.error:
            audit_log=Audit.objects.get(user=UserProfile.objects.get(email=self.message.user),channel=self.message.reply_channel.name)
            audit_log.is_finished = True
            audit_log.end_time = now()
            audit_log.save()
            self.closessh()
            self.close()
        except Exception,e:
            import traceback
            print traceback.print_exc()
            self.closessh()
            self.close()


class SshTerminalMonitor(WebsocketConsumer):

    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True


    def connect(self, message,channel):
        self.message.reply_channel.send({"accept": True})
        #permission auth
        Group(channel).add(self.message.reply_channel.name)

    def disconnect(self, message,channel):
        Group(channel).discard(self.message.reply_channel.name)
        self.message.reply_channel.send({"accept":False})
        self.close()

    def receive(self,text=None, bytes=None, **kwargs):
        pass