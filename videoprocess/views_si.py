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

def genCamera(fileName, sharedVar, recognizer):
    # count = 1
    vcap = videocap.VideoCap(fileName)

    last_emotion=''
    recognizer.start()
    while(True):
        if(not vcap.opened):
            return


        ret, frame = vcap.getCap().read()

        sharedVar.setImage(frame)

        if(not ret):
            return

        if(tconsumers.web_skt is None):
            print('gen returned')
            return
        # np_array = np.fromstring(frame, np.uint8)
        # img_np=cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        # results = recognition.emotion_recognize(frame)
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

        if tconsumers.started:
            current_time=datetime.datetime.now()
            if info_returned!='':
                message.objects.create(time=current_time, info=info_returned)
            tconsumers.web_skt.send(info_returned)


        image = cv2.imencode('.jpg', frame)[1]
        chunkheader = b"Content-Type: image/jpeg\nContent-Length: " + str(len(image)).encode('ascii') + b"\n\n"
        boundary = b"\n--myboundary\n"
        yield (chunkheader + bytearray(image) + boundary)
        time.sleep(0.05)


def mjpeg(request):
    print('mjpeg called')
    return StreamingHttpResponse(genCamera(), content_type='multipart/x-mixed-replace;boundary=myboundary')

def recognizer_function(sharedVar):
    while True:
        sharedVar.setRes(recognition.emotion_recognize(sharedVar.img))
        time.sleep(0.05)

def playVideo(request, fileName):
    # cap = videocap.VideoCap(fileName)
    # print('playVideo called')
    # return StreamingHttpResponse(genCamera(cap), content_type='multipart/x-mixed-replace;boundary=myboundary')
    sharedVar = mp.sharedVar()
    recognizer = threading.Thread(target = recognizer_function, args = (sharedVar,))

    # trd = threading.Thread(target = giveMsg, args = (0,))
    # trd.start()
    return StreamingHttpResponse(genCamera(fileName, sharedVar, recognizer),  content_type='multipart/x-mixed-replace;boundary=myboundary')

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
    if request.method == 'GET':
        usr_name = ''
        super_user = 'hidden'
        if request.session.get('logstate') == 'logged':
            usr_name = request.session.get('usrname')
            usr = User.objects.get(username=usr_name)
            if usr.is_superuser:
                super_user = ''
            return render(request, 'info.html', {'usr_name': usr_name, 'super_user': super_user})
        else:
            return HttpResponse(status=403)

