# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.count = 1
    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
#       text_data_json = json.loads(text_data)
#        message = text_data_json['message']

#        self.send(text_data=json.dumps({
#            'message': message
#        }))
        
        print('---------------\n' + text_data)
        self.send('hello!' + str(self.count))
        self.count += 1
        if(self.count == 20):
            self.close()