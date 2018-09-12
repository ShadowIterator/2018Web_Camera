

class sharedVar:
    def __init__(self):
        self.img = None
        self.res = []
        self.started = False
        pass

    def __del__(self):
        pass

    def setImage(self, image):
        self.img = image

    def setRes(self, result):
        self.res = result
