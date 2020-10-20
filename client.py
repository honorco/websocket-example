try:
    import thread
except ImportError:
    import _thread as thread
import websocket
import json


class ClientConnector:
    def __init__(self):
        self.ws = websocket.WebSocketApp("ws://localhost:8765", on_message=self.on_message)
        self.routes = {}

    def on_message(self, message):
        message = json.loads(message)
        if message['url'] and self.routes[message['url']]:
            self.routes[message['url']]()

    def send(self, url, msg):
        self.ws.send(json.dumps({"url": url, "msg": msg}))

    def run2(self):
        thread.start_new_thread(lambda: self.ws.run_forever(), ())


class ChatController:
    def __init__(self, connector):
        self.connector = connector

    def list(self):
        self.connector.send('/chats/list', [1, 2, 3])

    def create(self):
        self.connector.send('/chats/create', 'ok')


websocket.enableTrace(True)
c = ClientConnector()
chatController = ChatController(c)
c.routes = {
    "/chats/list": chatController.list,
    "/chats/create": chatController.create
}
c.run2()
while True:
    c.send('/chats/list', input())
