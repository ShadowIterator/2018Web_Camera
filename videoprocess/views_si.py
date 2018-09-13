from django.shortcuts import render

import cv2
import numpy as np
import threading
import base64
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from . import recognition
from . import videocap
import time
from . import mp

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
    recognizer.start()
    while(True):
        if(not vcap.opened):
            return


        ret, frame = vcap.getCap().read()

        sharedVar.setImage(frame)

        if(not ret):
            return

        # np_array = np.fromstring(frame, np.uint8)
        # img_np=cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        # results = recognition.emotion_recognize(frame)
        results = sharedVar.res

        for result in results:
            result.drawToImage(frame)

        image = cv2.imencode('.jpg', frame)[1]
        chunkheader = b"Content-Type: image/jpeg\nContent-Length: " + str(len(image)).encode('ascii') + b"\n\n"
        boundary = b"\n--myboundary\n"
        yield (chunkheader + bytearray(image) + boundary)
        time.sleep(0.01)

def mjpeg(request):
    print('mjpeg called')
    return StreamingHttpResponse(genCamera(), content_type='multipart/x-mixed-replace;boundary=myboundary')

def recognizer_function(sharedVar):
    while True:
        sharedVar.setRes(recognition.emotion_recognize(sharedVar.img))

def playVideo(request, fileName):
    # cap = videocap.VideoCap(fileName)
    # print('playVideo called')
    # return StreamingHttpResponse(genCamera(cap), content_type='multipart/x-mixed-replace;boundary=myboundary')
    sharedVar = mp.sharedVar()
    recognizer = threading.Thread(target = recognizer_function, args = (sharedVar,))
    return StreamingHttpResponse(genCamera(fileName, sharedVar, recognizer),  content_type='multipart/x-mixed-replace;boundary=myboundary')

def releaseCap(request):
    print ('released!')
    # glb_cap.release()
    return render(request, 'login.html')

def websocket(request):
	return render(request,
		  'websocket.html',
		  {}
		  )