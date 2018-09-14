from django.shortcuts import render

import cv2
import numpy as np
import threading
import base64
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from . import recognition
from .models import message
import time


# Create your views here.
#cap=cv2.VideoCapture(0)
#cap = cv2.VideoCapture(0)

def start_camera():
    ret, frame=cap.read()
    cv2.imwrite('frame.png', frame)


# def show_frame(request):
#     if request.method=='GET':
#         return render(request,'index.html')
#     elif request.method=='POST':
#         global cap
#         ret, frame = cap.read()
#         # np_array = np.fromstring(frame, np.uint8)
#         # img_np=cv2.imdecode(np_array, cv2.IMREAD_COLOR)
#
# #        recognized_image=recognition.emotion_recognize(frame)
# #        image = cv2.imencode('.png', recognized_image)[1]
#         image = cv2.imencode('.png', frame)[1]
#         response = HttpResponse(str(base64.b64encode(image))[2:-1])
#         response['Access-Control-Allow-Origin'] = '*'
#         return response
def sign_up(request):
    if request.method=='GET':

        return render(request, 'signup.html')
    elif request.method=='POST':
        usr_name=request.POST.get('username')
        usr_password=request.POST.get('password')
        usr_confirm=request.POST.get('confirm')

        if User.objects.filter(username=usr_name):
            instruction = '用户已存在，请直接登录'
            return render(request, 'signup.html', {'instruction': instruction})
        # if authenticate(username=usr_name):
        #     instruction='用户已存在，请直接登录'
        #     return render(request, 'signup.html', {'instruction':instruction})
        if usr_password==usr_confirm:
            User.objects.create_user(username=usr_name, password=usr_password)
            return redirect('/video/login')
        else:
            instruction='请重新确认密码'
            return render(request, 'signup.html', {'instruction':instruction})

def log_in(request):
    if request.method=='GET':
        return render(request, 'login.html')
    elif request.method=='POST':
        usr_name=request.POST.get('username')
        usr_password=request.POST.get('password')

        if User.objects.filter(username=usr_name):
            possible_user = User.objects.get(username=usr_name)
            if possible_user.check_password(usr_password):
                request.session['logstate']='logged'
                request.session['usrname']=usr_name
                request.session.set_expiry(0)
                return redirect('/video/info')
            else:
                instruction='密码不正确，请重新登录'
                return render(request, 'login.html', {'instruction':instruction})
        else:
            instruction='用户不存在，请先注册'
            return render(request, 'login.html', {'instruction':instruction})

def log_out(request):
    request.session.flush()
    return redirect('/video/login')

def manage_user(request):
    if request.method=='GET':
        show_users=[]
        all_users=User.objects.all()
        for user in all_users:
            if not user.is_superuser:
                show_users.append(user)
        return render(request, 'manage.html', {'show_users': show_users})

def delete_user(request):
    if request.method=='POST':
        for each_user in User.objects.all():
            if request.POST.get(str(each_user.id)):
                each_user.delete()
        return redirect('/video/manage')

def add_user(request):
    if request.method=='POST':
        usr_name=request.POST.get('username')
        usr_password=request.POST.get('password')
        User.objects.create_user(username=usr_name, password=usr_password)
        return redirect('/video/manage')

def manage_record(request):
    if request.method=='GET':
        all_records=message.objects.all()
        return render(request, 'record.html', {'records':all_records})

def del_record(request):
    if request.method=='POST':
        if request.POST.get('single_del'):
            for single_record in message.objects.all():
               if request.POST.get(str(single_record.id)):
                   single_record.delete()
        elif request.POST.get('del_all'):
            for single_record in message.objects.all():
                single_record.delete()
        return redirect('/video/records')
