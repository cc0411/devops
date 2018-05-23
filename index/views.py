# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import  auth
from index import  models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView

# Create your views here.

@login_required()
def Dashboard(request):
    return  render(request,'dashboard.html')

@login_required()
def index(request):
    return  render(request,'index.html')

def login(request):
    err_msg = ''
    if request.method == 'GET':
        return render(request, 'login.html', {'err_msg': err_msg})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        u = auth.authenticate(email=username, password=password)
        if u:
            auth.login(request, u)
            request.session['is_login'] = True
            request.session.set_expiry(3600)
            login_ip = request.META['REMOTE_ADDR']
            models.Loginlog.objects.create(user=request.user, ip=login_ip, action="***login***")

            return redirect('/')
        else:
            return render(request, 'login.html', {'err_msg': '邮箱账号或密码错误'})

    return render(request, 'login.html', {'err_msg': err_msg})

@login_required()
def logout(request):
    login_ip = request.META['REMOTE_ADDR']
    models.Loginlog.objects.create(user=request.user, ip=login_ip, action="***logout***")
    request.session.clear()
    auth.logout(request)
    return redirect('/')

class LoginLogList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    template_name = 'loginlog.html'
    model = models.Loginlog
    context_object_name =  "session_list"
    queryset = models.Loginlog.objects.all()
    ordering = ('-id'),
    permission_required = 'index.can_view_loginlog'
    raise_exception = True
