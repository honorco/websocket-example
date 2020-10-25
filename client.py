try:
    import thread
except ImportError:
    import _thread as thread
import websocket
import json


class ClientConnector:
    def __init__(self, url, port, routes):
        self.routes = routes
        self.ws = websocket.WebSocketApp(f"ws://{url}:{port}", on_message=self.on_message)
        thread.start_new_thread(lambda: self.ws.run_forever(), ())

    def on_message(self, message):
        print(message)
        message = json.loads(message)
        if message['url'] and message['data'] and self.routes[message['url']]:
            self.routes[message['url']](self, message['data'])

    def send(self, url, msg):
        self.ws.send(json.dumps({"url": url, "data": msg}))


class MessageController:
    @staticmethod
    def create(self, data):
        print(data)


connector = ClientConnector('localhost', 8765, {
    "/messages/create": MessageController.create,
})

while True:
    connector.send('/messages/create', input())
