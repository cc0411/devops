# -*- coding: utf-8 -*-

from django.views.generic import View
from django.shortcuts import render_to_response,render
from django.http import JsonResponse
from asset.models import HostGroup
from jump.models import Audit
try:
    import simplejson as json
except ImportError:
    import json
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.encoding import smart_str
from django.views.generic.list import ListView

from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

from devops.settings import MEDIA_URL
from django.utils.timezone import now
from devops.interactive import get_redis_instance
# Create your views here.

class Index(LoginRequiredMixin,View):

    def get(self,request):

        return render(request,'jump/index.html')

class SshLogList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Audit
    template_name = 'jump/auditlogs.html'
    permission_required = 'jump.can_view_log'
    context_object_name = "audit_list"
    queryset =  Audit.objects.all()
    raise_exception = True
    ordering = ('-id'),

class SshLogPlay(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    model = Audit
    template_name = 'jump/auditplay.html'
    permission_required = 'jump.can_play_log'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(SshLogPlay, self).get_context_data(**kwargs)
        objects = kwargs['object']
        context['logpath'] = '{0}{1}-{2}-{3}/{4}.json'.format(MEDIA_URL,objects.start_time.year,objects.start_time.month,objects.start_time.day,objects.log)
        return context
class SshTerminalMonitor(LoginRequiredMixin,DetailView):
    model = Audit
    template_name = 'jump/auditmonitor.html'

class SshTerminalKill(LoginRequiredMixin,View):

    def post(self,request):
        if request.is_ajax():
            channel_name = request.POST.get('channel_name',None)
            try:
                data = Audit.objects.get(channel=channel_name)
                if data.is_finished:
                    return JsonResponse({'status':False,'message':'Ssh terminal does not exist!'})
                else:
                    data.end_time = now()
                    data.is_finished = True
                    data.save()

                    queue = get_redis_instance()
                    redis_channel = queue.pubsub()
                    queue.publish(channel_name, json.dumps(['close']))

                    return JsonResponse({'status':True,'message':'Terminal has been killed !'})
            except ObjectDoesNotExist:
                return JsonResponse({'status':False,'message':'Request object does not exist!'})