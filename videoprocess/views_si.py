from django.shortcuts import render

import cv2
import numpy as np
import threading
import base64
import datetime
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from . import recognition
from . import videocap
import time
from . import mp
from . import tconsumers
from .models import message

# global glb_cap

# Create your views here.
def genHtml():
    for x in range(10):
        yield str(x)
        time.sleep(1)

def welcome(request):
    return render(request,'welcome.html',{'testvar': 'welcome'})

def genCamera(fileName, sharedVar, recognizer, sessionID):
    # count = 1
    fileName = fileName.replace('{/questionmark}', '?')
    print(fileName)
    vcap = videocap.VideoCap(fileName)

    last_emotion=''
    recognizer.start()
    while(True):
        if(not vcap.opened):
            return
        # print('--------')
        ret, frame = vcap.getCap().read()

        sharedVar.setImage(frame)

        if(not ret):
            return

        if(tconsumers.seek_socket(sessionID) == 'NOTFOUND'):
            print('gen notfound')
            return

        results = sharedVar.res

        info_returned = ''

        for result in results:
            result.drawToImage(frame)
            info_returned += result.emotion_res+' '

        if len(results) == 1:
            if last_emotion == results[0].emotion_res:
                info_returned = ''
            else:
                last_emotion = results[0].emotion_res
        else:
            last_emotion=''

        socket = tconsumers.seek_socket(sessionID)

        if socket != 'UNKNOWN':
            current_time=datetime.datetime.now()
            if info_returned!='':
                message.objects.create(time=current_time, info=info_returned)
            socket.send(info_returned)
        else:
            print('gen unkwon')

        image = cv2.imencode('.jpg', frame)[1]
        chunkheader = b"Content-Type: image/jpeg\nContent-Length: " + str(len(image)).encode('ascii') + b"\n\n"
        boundary = b"\n--myboundary\n"
        yield (chunkheader + bytearray(image) + boundary)
        time.sleep(0.05)


def mjpeg(request):
    print('mjpeg called')
    return StreamingHttpResponse(genCamera(), content_type='multipart/x-mixed-replace;boundary=myboundary')

def recognizer_function(sharedVar, sessionID):
    while True:
        # print('recognizing')
        socket = tconsumers.seek_socket(sessionID)
        if(socket == 'NOTFOUND'):
            print('recg, notfound')
            return
        if(socket != 'UNKNOWN'):
            sharedVar.setRes(recognition.emotion_recognize(sharedVar.img))
        else:
            print('recg, unknown')
        time.sleep(0.05)

def playVideo(request, fileName):
    sessionID = request.session.session_key
    if(tconsumers.seek_socket(sessionID) != 'NOTFOUND'):
        return HttpResponse(status = 403)
    else:
        tconsumers.declare_socket(sessionID)

    sharedVar = mp.sharedVar()
    recognizer = threading.Thread(target = recognizer_function, args = (sharedVar, sessionID))

    return StreamingHttpResponse(genCamera(fileName, sharedVar, recognizer, sessionID),  content_type='multipart/x-mixed-replace;boundary=myboundary')

def releaseCap(request):
    print ('released!')
    # glb_cap.release()
    return render(request, 'login.html')

def giveMsg(x):
    while True:
        if(tconsumers.started):
            tconsumers.web_skt.send('websocket')
        time.sleep(0.7)

def websocket(request):
    trd = threading.Thread(target = giveMsg, args = (0,))
    trd.start()
    return render(request, 'websocket.html',{})

def infotest(request):
    # sessionID = request.session.session_key
    # if(tconsumers.seek_socket(sessionID) != 'NOTFOUND'):
    #     return HttpResponse(status = 403)

    if request.method == 'GET':
        usr_name = ''
        super_user = 'hidden'
        if request.session.get('logstate') == 'logged':
            usr_name = request.session.get('usrname')
            usr = User.objects.get(username=usr_name)
            if usr.is_superuser:
                super_user = ''
            return render(request, 'info.html', {'usr_name': usr_name, 'super_user': super_user, 'session_id': str(request.session.session_key)})
        else:
            return HttpResponse(status=403)

def resetPwd(request):
    sessionID = request.session.session_key

    usr_name = request.session.get('usrname')
    usr = User.objects.get(username = usr_name)
    oldPwd = request.POST.get('oldpwd')
    newPwd = request.POST.get('newpwd')
    rptnewPwd = request.POST.get('rptnewpwd')
    super_user = 'hidden'
    if usr.is_superuser:
        super_user = ''
    if(usr.check_password(oldPwd)):
        if(newPwd == rptnewPwd):
            usr.set_password(newPwd)
            usr.save()
            print(newPwd)
            return render(request, 'info.html', {'usr_name': usr_name, 'super_user': super_user, 'resetpwd_result': 'reset password success', 'session_id': str(request.session.session_key)})
        else:
            return render(request, 'info.html', {'usr_name': usr_name, 'super_user': super_user, 'resetpwd_result': '两次输入的密码不一样', 'session_id': str(request.session.session_key)})
    else:
        return render(request, 'info.html',
                      {'usr_name': usr_name, 'super_user': super_user, 'resetpwd_result': '密码错误', 'session_id': str(request.session.session_key)})

