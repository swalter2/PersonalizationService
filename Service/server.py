from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from service import service

http_server = HTTPServer(WSGIContainer(service))
http_server.listen(5000, address='127.0.0.1')
IOLoop.instance().start()

