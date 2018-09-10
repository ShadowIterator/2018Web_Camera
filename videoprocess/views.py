from django.shortcuts import render

import cv2
import numpy as np
import threading
import base64
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from . import recognition
import time


# Create your views here.
cap=cv2.VideoCapture('No6.mp4')
#cap = cv2.VideoCapture(0)

def start_camera():
    ret, frame=cap.read()
    cv2.imwrite('frame.png', frame)

def genHtml():
    for x in range(10):
        yield str(x)
        time.sleep(1)

def welcome(request):
    return render(request,'welcome.html',{'testvar': 'welcome'})
		
def genCamera(cap):
    count = 1
#    global cap
    while(True):
        ret, frame = cap.read()
		
        np_array = np.fromstring(frame, np.uint8)
        img_np=cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        frame = recognition.emotion_recognize(frame)
        image = cv2.imencode('.jpg', frame)[1]
        chunkheader = b"Content-Type: image/jpeg\nContent-Length: " + str(len(image)).encode('ascii') + b"\n\n"
        boundary = b"\n--myboundary\n"
        print(count)
        count += 1
        yield (chunkheader + bytearray(image) + boundary)
        time.sleep(0.04)

def mjpeg(request):
#    if request.method=='GET':
#        return render(request,'mjpeg.html')
    print('mjpeg called')
    return StreamingHttpResponse(genCamera(), content_type='multipart/x-mixed-replace;boundary=myboundary')
#    return StreamingHttpResponse(genHtml())

def playSaiki(request):
#    if request.method=='GET':
#        return render(request,'mjpeg.html')
    cap = cv2.VideoCapture('saiki.mkv')
    print('playSaiki called')
    return StreamingHttpResponse(genCamera(cap), content_type='multipart/x-mixed-replace;boundary=myboundary')
#    return StreamingHttpResponse(genHtml())


def playVideo(request, fileName):
#    if request.method=='GET':
#        return render(request,'mjpeg.html')
    if(fileName == 'camera'):
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(fileName)
    print('playVideo called')
    return StreamingHttpResponse(genCamera(cap), content_type='multipart/x-mixed-replace;boundary=myboundary')
#    return StreamingHttpResponse(genHtml())

def show_frame(request):
    if request.method=='GET':
        return render(request,'index.html')
    elif request.method=='POST':
        global cap
        ret, frame = cap.read()
        # np_array = np.fromstring(frame, np.uint8)
        # img_np=cv2.imdecode(np_array, cv2.IMREAD_COLOR)

#        recognized_image=recognition.emotion_recognize(frame)
#        image = cv2.imencode('.png', recognized_image)[1]
        image = cv2.imencode('.png', frame)[1]
        response = HttpResponse(str(base64.b64encode(image))[2:-1])
        response['Access-Control-Allow-Origin'] = '*'
        return response
def sign_up(request):
    if request.method=='GET':
        return render(request, 'signup.html')
    elif request.method=='POST':
        usr_name=request.POST.get('username')
        usr_password=request.POST.get('password')
        usr_email=request.POST.get('email')
        User.objects.create_user(username=usr_name, password=usr_password)

        return redirect('/video/refresh')
