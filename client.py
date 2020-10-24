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
        print(message)
        message = json.loads(message)
        if message['url'] and message['data'] and self.routes[message['url']]:
            self.routes[message['url']](self, message['data'])

    def send(self, url, msg):
        self.ws.send(json.dumps({"url": url, "data": msg}))

    def run(self):
        thread.start_new_thread(lambda: self.ws.run_forever(), ())


class ChatController:
    @staticmethod
    def create(self, data):
        print(data)


connector = ClientConnector({
    "/messages/create": ChatController.create,
})
connector.run()

while True:
    connector.send('/messages/create', input())
