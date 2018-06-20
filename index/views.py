# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import  auth
from index import  models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView,View
from django_otp import match_token
# Create your views here.
import  json

@login_required()
def Dashboard(request):
    return  render(request,'dashboard.html')

@login_required()
def index(request):
    return  render(request,'index.html')
class LoginView2(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        ret = {"status":True,"msg":""}

        username = request.POST.get('username')
        password = request.POST.get('password')
        valid_code = request.POST.get('valid_code')
        code_session =request.session.get("valid_code","")
        if valid_code  and valid_code.upper() ==code_session.upper():
            u = auth.authenticate(email = username,password=password)
            if u:
                auth.login(request,u)
                request.session['is_login'] = True
                request.session.set_expiry(3600)
                login_ip = request.META['REMOTE_ADDR']
                models.Loginlog.objects.create(user=request.user, ip=login_ip, action="***login***")
                ret["msg"] = "登录成功"
            else:
                ret['status'] = False
                ret['msg'] = "用户名或者密码错误"
        else:
            ret["status"] = False
        ret['msg'] = "验证码错误"
        return  JsonResponse(ret)
class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})
    def post(self,request):
        ret = {"status":False,'msg':None}
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_len = len(password)
        valid_code = request.POST.get('valid_code')
        code_session =request.session.get("valid_code","")
        if valid_code  and valid_code.upper() ==code_session.upper():
            if password_len <=6:
                ret['msg'] = "密码输入错误，请重新输入"
            qrcode = password[-6:]
            password = password[:password_len-6]
            u = auth.authenticate(email = username,password=password)
            if u:
                if match_token(u,qrcode)!= None:
                    auth.login(request, u)
                    request.session['is_login'] = True
                    request.session.set_expiry(3600)
                    login_ip = request.META['REMOTE_ADDR']
                    models.Loginlog.objects.create(user=request.user, ip=login_ip, action="***login***")
                    ret["status"] = True
            else:
                ret['msg'] = "用户名或者密码错误"
        else:
            ret['msg'] = "验证码错误"
        return  JsonResponse(ret)


def get_valid_img(request):
    # with open("valid_code.png", "rb") as f:
    #     data = f.read()
    # 自己生成一个图片
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (180, 34),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("static/fonts/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(4):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20+40*i, 0), tmp, fill=get_random_color(), font=font_obj)

    print("".join(tmp_list))
    print("生成的验证码".center(120, "="))
    # 不能保存到全局变量
    # global VALID_CODE
    # VALID_CODE = "".join(tmp_list)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    width = 180  # 图片宽度（防止越界）
    height = 34
    # for i in range(5):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    #
    # # 加干扰点
    # for i in range(40):
    #     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    # 将生成的图片保存在磁盘上
    # with open("s10.png", "wb") as f:
    #     img_obj.save(f, "png")
    # # 把刚才生成的图片返回给页面
    # with open("s10.png", "rb") as f:
    #     data = f.read()

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    from io import BytesIO
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)

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
