import time
from typing import List, Tuple, Dict
from collections.abc import Callable

try:
    import thread
except ImportError:
    import _thread as thread
from abc import ABC
import tornado.web
import tornado.websocket
import tornado.ioloop
import json
import asyncio

callbacks: Dict[int, Callable] = {}
clients = []


class MessageController:
    @staticmethod
    def create(self, data):
        for client in [c for c in clients if c != self]:
            client.send('/messages/create', data)

    @staticmethod
    def get(self, data):
        return "this is data"


routes = {
    "/messages/create": MessageController.create,
    "/messages/get": MessageController.get
}


class ServerConnector(tornado.websocket.WebSocketHandler, ABC):
    def open(self):
        clients.append(self)
        print("WebSocket opened")

    def on_message(self, message: str):
        print(message)
        message: Dict = json.loads(message)
        server_id = message.get('server_id')
        client_id = message.get('client_id')
        url = message.get('url')
        if url and client_id:
            handler = routes.get(url)
            res = handler(self, message.get('data')) or None
            self.write_message(json.dumps({"client_id": client_id, "data": res}))
        elif url:
            handler = routes.get(url)
            handler(self, message.get('data'))
        elif server_id:
            handler = callbacks.pop(server_id)
            handler(self, message.get('data'))

    def send(self, url, message=None, callback=None):
        res = {"url": url}
        if message:
            res["data"] = message
        if callback:
            server_id = time.time_ns()
            res['server_id'] = server_id
            callbacks[server_id] = callback
        self.write_message(json.dumps(res))

    def on_close(self):
        clients.remove(self)
        print("WebSocket closed")


def initServer():
    asyncio.set_event_loop(asyncio.new_event_loop())
    application = tornado.web.Application([(r"/", ServerConnector)])
    application.listen(8765, '0.0.0.0')
    try:
        loop = tornado.ioloop.IOLoop.current()
        loop.start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()


thread.start_new_thread(initServer, ())

while True:
    msg = input()
    clients[0].send('check', callback=lambda self, x: print(x))
