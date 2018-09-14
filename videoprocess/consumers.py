# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from . import tconsumers



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.count = 1
        global web_skt
        global started
        tconsumers.web_skt = self
        tconsumers.started = True

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):

        print('---------------\n' + text_data)
        self.send('hello!' + str(self.count))
        self.count += 1
        # if(self.count == 20):
        #     self.close()


class InfoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.count = 0


    def disconnect(self, close_code):
        print('drop')
        tconsumers.drop_socket(self.sessionID)

    def receive(self, text_data):
        print('recv')
        self.sessionID = text_data
        tconsumers.register_socket(text_data, self)
        print('---------------\n' + text_data)

