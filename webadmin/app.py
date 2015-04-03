# coding:utf-8
import os

import redis
import torndb
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import options, define

import webapp
import settings


class MyApplication(Application):
    def __init__(self):
        handlers = [
            (r"/", webapp.IndexHandler),
            (r"/list", webapp.ListHandler),
            (r"/detail", webapp.DetailHandler),
            (r"/download", webapp.DownloadHandler)
        ]
        config = dict(
            template_path=os.path.join(os.path.dirname(__file__), settings.TEMPLATE_ROOT),
            static_path=os.path.join(os.path.dirname(__file__), settings.STATIC_ROOT),
            #xsrf_cookies=True,
            cookie_secret="__TODO:_E720135A1F2957AFD8EC0E7B51275EA7__",
            autoescape=None,
            debug=settings.DEBUG
        )
        Application.__init__(self, handlers, **config)

        self.redis = redis.Redis(**settings.REDIS)
        self.db = torndb.Connection(**settings.DATABASE)


def run():
    options.parse_command_line()
    define("host", default=settings.HOST, help="Served host")
    define("port", default=settings.PORT, help="Served port", type=int)
    http_server = HTTPServer(MyApplication())
    http_server.listen(port=options.host, address=options.port)

    IOLoop.instance().start()


if __name__ == '__main__':
    run()
