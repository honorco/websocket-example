import time
from collections.abc import Callable
from typing import Dict

try:
    import thread
except ImportError:
    import _thread as thread
import websocket    # pip install websocket-client
import json

callbacks: Dict[int, Callable] = {}


class ClientConnector:
    def __init__(self, url, port, routes):
        self.routes = routes
        self.ws = websocket.WebSocketApp(f"ws://{url}:{port}", on_message=self.on_message)
        thread.start_new_thread(lambda: self.ws.run_forever(), ())

    def on_message(self, message):
        print(message)
        message: Dict = json.loads(message)
        server_id = message.get('server_id')
        client_id = message.get('client_id')
        url = message.get('url')
        if url and server_id:
            handler = self.routes.get(url)
            res = handler(self, message.get('data')) or None
            self.ws.send(json.dumps({"server_id": server_id, "data": res}))
        elif url:
            handler = self.routes.get(url)
            handler(self, message.get('data'))
        elif client_id:
            handler = callbacks.pop(client_id)
            handler(self, message.get('data'))

    def send(self, url, message=None, callback=None):
        res = {"url": url}
        if message:
            res["data"] = message
        if callback:
            client_id = time.time_ns()
            res['client_id'] = client_id
            callbacks[client_id] = callback
        self.ws.send(json.dumps(res))










class MessageController:
    @staticmethod
    def create(connector, data):
        print(data)

    @staticmethod
    def check(connector, data):
        return 'hello, bro!'


connector = ClientConnector('localhost', 8765, {
    "/messages/create": MessageController.create,
    "check": MessageController.check
})

while True:
    input()
    connector.send('/messages/get', callback=lambda self, x: print(x))
    connector.send('/messages/get', 'dataaaa')
