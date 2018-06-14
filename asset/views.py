# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView, DetailView
from asset import  models,forms
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import xlwt,time
import  csv,codecs
from io import StringIO
from datetime import date, datetime
import  json
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
class AssetList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    template_name = 'asset/host.html'
    model = models.Assets
    context_object_name =  "asset_list"
    queryset = models.Assets.objects.all()
    ordering = ('-id'),
    permission_required = 'asset.can_view_asset'
    raise_exception = True

class  GetAssetJson(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        rows =[]
        total = models.Assets.objects.all().count()
        queryset = models.Assets.objects.all()
        for row in queryset:
            rows.append ({'pk':row.pk,'hostname':row.hostname,'wip':row.wip,'lip':row.lip,'system_type':row.system_type,'ctime':row.ctime,'utime':row.utime,'idc':[i.name for i in row.idc_set.all()],'group':[g.name for g in row.hostgroup_set.all()],'status':row.get_online_status_display()},
                   )
        data = {"total":total,'rows':rows}
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder,ensure_ascii=False), content_type="application/json")

class HostGroupList(LoginRequiredMixin,PermissionRequiredMixin,ListView):

    template_name = 'asset/roles.html'
    model = models.HostGroup
    context_object_name = "group_list"
    queryset =  models.HostGroup.objects.all()
    ordering = ('-id'),
    permission_required = 'asset.can_view_hostgroup'
    raise_exception = True

class  IdcList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    template_name = 'asset/idc.html'
    model =  models.IDC
    context_object_name = "idc_list"
    queryset = models.IDC.objects.all()
    ordering = ('-id'),
    permission_required = 'asset.can_view_idc'
    raise_exception = True

class HostUserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'asset/user.html'
    model = models.HostUsers
    context_object_name = "user_list"
    queryset = models.HostUsers.objects.all()
    ordering = ('-id'),
    permission_required = 'asset.can_view_hostuser'
    raise_exception = True

class AssetAdd(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.Assets
    form_class =forms.AssetForm
    template_name =  'asset/asset_add.html'
    success_url = reverse_lazy('asset_list')
    permission_required = 'asset.can_add_asset'
    raise_exception = True


class GostGroupAdd(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.HostGroup
    form_class = forms.HostGroupForm
    template_name =  'asset/role_add.html'
    success_url = reverse_lazy('role_list')
    permission_required = 'asset.can_add_hostgroup'
    raise_exception = True

class IdcAdd(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.IDC
    form_class =  forms.IDCForm
    template_name = 'asset/idc_add.html'
    success_url = reverse_lazy('idc_list')
    permission_required = 'asset.can_add_idc'
    raise_exception = True


class HostUserAdd(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.HostUsers
    form_class = forms.HostUserForm
    template_name = 'asset/user_add.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'asset.can_add_hostuser'
    raise_exception = True


class AssetUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Assets
    form_class = forms.AssetForm
    template_name = 'asset/asset_add.html'
    success_url = reverse_lazy('asset_list')
    permission_required = 'asset.can_change_asset'
    raise_exception = True

    def form_invalid(self, form):
        return super(AssetUpdate, self).form_invalid(form)


class HostGroupUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.HostGroup
    form_class = forms.HostGroupForm
    template_name = 'asset/role_add.html'
    success_url = reverse_lazy('role_list')
    permission_required = 'asset.can_change_hostgroup'
    raise_exception = True

    def form_invalid(self, form):
        return super(HostGroupUpdate, self).form_invalid(form)


class IdcUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.IDC
    form_class = forms.IDCForm
    template_name = 'asset/idc_add.html'
    success_url = reverse_lazy('idc_list')
    permission_required = 'asset.can_change_idc'
    raise_exception = True

    def form_invalid(self, form):
        return super(IdcUpdate, self).form_invalid(form)


class HostUserUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.HostUsers
    form_class = forms.HostUserForm
    template_name = 'asset/user_add.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'asset.can_change_hostuser'
    raise_exception = True

    def form_invalid(self, form):
        return super(HostUserUpdate, self).form_invalid(form)

import  json
class AssetDel(LoginRequiredMixin,View):
    model = models.Assets
    @staticmethod
    def post(request):
        ret = {'status':True,'error':None}
        try:
            if request.POST.get('nid'):
                ids = request.POST.get('nid',None)
                models.Assets.objects.get(id=ids).delete()
            else:
                ids = request.POST.getlist('id',None)
                idstring = ','.join(ids)
                models.Assets.objects.extra(where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status']= False
            ret['error'] = '没有权限'
        finally:
            return HttpResponse(json.dumps(ret))
@login_required()
def export(request):
    if request.method == "GET":
        asset_list = models.Assets.objects.all()
        bt = ['ID','主机名','外网地址','内网地址','系统类型','机房','ServerID','GameID','角色','创建时间','更新时间','是否启用','备注']
        wb = xlwt.Workbook(encoding='utf-8')
        sh = wb.add_sheet("主机详情",cell_overwrite_ok=True)
        dateFormat = xlwt.XFStyle()
        dateFormat.num_format_str = 'yyyy/mm/dd'
        for i in range(len(bt)):
            sh.write(0,i,bt[i])
        for i in range(len(asset_list)):
            sh.write(i + 1, 0, asset_list[i].id)
            sh.write(i + 1, 1, asset_list[i].hostname)
            sh.write(i + 1, 2, asset_list[i].wip)
            sh.write(i + 1, 3, asset_list[i].lip)
            sh.write(i + 1, 4, asset_list[i].system_type)
            for idc in asset_list[i].idc_set.all():
                sh.write(i + 1, 5, idc.name)
            sh.write(i + 1, 6, asset_list[i].serverid)
            sh.write(i + 1, 7, asset_list[i].gameid)
            for g in asset_list[i].hostgroup_set.all():
                sh.write(i + 1, 8, g.name)
            sh.write(i + 1, 9, asset_list[i].ctime,dateFormat)
            sh.write(i + 1, 10, asset_list[i].utime,dateFormat)
            sh.write(i + 1, 11, asset_list[i].get_online_status_display())
            sh.write(i + 1, 12, asset_list[i].memo)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=asset' + time.strftime('%Y%m%d', time.localtime(
                time.time())) + '.xls'
        wb.save(response)

        return response


@login_required()
def idc_asset(request, nid):
    obj = models.IDC.objects.get(id=nid)
    return render(request, 'asset/idc_asset.html', {"nid": nid, "asset_list": obj,})


@login_required()
def group_asset(request, nid):
    obj = models.HostGroup.objects.get(pk=nid)
    return render(request, 'asset/group_asset.html', {"nid": nid, "asset_list": obj,})

















