import cv2

class VideoCap:
    def __init__(self, fileName):
        if(fileName == 'camera' or fileName == ''):
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(fileName)
        self.opened = True

    def __del__(self):
        self.cap.release()
        self.opened = False
        print('deleted')

    def getCap(self):
        return self.cap