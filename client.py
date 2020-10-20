try:
    import thread
except ImportError:
    import _thread as thread
import websocket
import json


class ClientConnector:
    def __init__(self, roures):
        self.ws = websocket.WebSocketApp("ws://localhost:8765", on_message=self.on_message)
        self.routes = roures

    def on_message(self, message):
        message = json.loads(message)
        if message['url'] and message['data'] and self.routes[message['url']]:
            self.routes[message['url']](message['data'])

    def send(self, url, msg):
        self.ws.send(json.dumps({"url": url, "data": msg}))

    def run(self):
        thread.start_new_thread(lambda: self.ws.run_forever(), ())


class ChatController:
    @staticmethod
    def list(data):
        print('list data: ' + data)

    @staticmethod
    def create(data):
        print('create data: ' + data)


connector = ClientConnector({
    "/chats/list": ChatController.list,
    "/chats/create": ChatController.create
})
connector.run()

while True:
    connector.send('/chats/list', input())
