# coding:utf-8
import os

import redis
import torndb
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import options

import webapp


class MyApplication(Application):
    def __init__(self, settings):
        handlers = [
            (r"/", webapp.IndexHandler),
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


def run(config):
    options.parse_command_line()

    http_server = HTTPServer(MyApplication(config))
    http_server.listen(port=config.PORT, address=config.HOST)

    IOLoop.instance().start()


if __name__ == '__main__':
    run()
