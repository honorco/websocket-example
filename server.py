from abc import ABC
import tornado.web
import tornado.websocket
import tornado.ioloop

clients = []


class ServerConnector(tornado.websocket.WebSocketHandler, ABC):
    def open(self):
        clients.append(self)
        print("WebSocket opened")

    def on_message(self, message):
        print(message)
        for client in [c for c in clients if c != self]:
            client.write_message(message)

    def on_close(self):
        clients.remove(self)
        print("WebSocket closed")


application = tornado.web.Application([(r"/", ServerConnector)])
application.listen(8765, '127.0.0.1')
try:
    loop = tornado.ioloop.IOLoop.current()
    loop.start()
except KeyboardInterrupt:
    tornado.ioloop.IOLoop.current().stop()
