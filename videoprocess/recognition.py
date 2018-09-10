import cv2
import numpy as np
import keras
import tensorflow as tf
from keras.models import load_model

emotion_model=load_model('./videoprocess/simple_CNN.985-0.66.hdf5')
graph=tf.get_default_graph()
face_cascade=cv2.CascadeClassifier('./videoprocess/haarcascade_frontalface_default.xml')


emotions={
    0: 'angry',
    1: 'disgust',
    2: 'fear',
    3: 'happy',
    4: 'sad',
    5: 'surprised',
    6: 'neutral'
}

def find_faces(image):
    gray_image=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray_image,
                                          scaleFactor=1.15,
                                          minNeighbors=5,
                                          minSize=(5, 5))
    return faces

def emotion_recognize(image):
    global graph
    with graph.as_default():
        face_pos=find_faces(image)
        gray_image=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        for (x,y,w,h) in face_pos:
            face=gray_image[y:y+h, x:x+w]
            face=cv2.resize(face,(48,48))
            face=face/255.0
            face=np.expand_dims(face,0)
            face=np.expand_dims(face,-1)
            emotion_label=np.argmax(emotion_model.predict(face))
            emotion_res=emotions[emotion_label]

            x,y,w,h=int(x), int(y), int(w), int(h)
            cv2.rectangle(image, (x, y), (x+w, y+h), (255,255,255), 2)
            text_font=cv2.FONT_HERSHEY_PLAIN
            cv2.putText(image,emotion_res, (x-10, y-10), text_font, 1.0, (255,255,255), 1)
        return image