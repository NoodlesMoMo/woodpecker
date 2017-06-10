#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动服务
"""
# sys
import logging
import os
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=9981, help="run on this port", type=int)
define("debug", default=True, help="enable debug mode")
define("runmode", default="test", help="test prod")
define("project_path", default=sys.path[0], help="deploy_path")
tornado.options.parse_command_line()

if options.debug:
    import tornado.autoreload

from handler.healthy import HealthyHandler


class Application(tornado.web.Application):
    """
    应用类
    """
    def __init__(self):
        """
        应用初始化
        """
        # 应用配置
        settings = {
            "site_title": "demo",
            "project_path": os.path.join(options.project_path),
            "static_path": os.path.join(options.project_path, "static"),
            "template_path": os.path.join(options.project_path, "tpl"),
            "xsrf_cookies": False,
            "debug": options.debug,
            "runmode": options.runmode,
        }

        # 处理器配置
        handlers = [
            (r"/healthy(/[a-z_A-Z/]*)?", HealthyHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

    def log_request(self, handler):
        """
        定制如何记录日志
        :param object handler: request handler
        """
        status = handler.get_status()
        if status < 400:
            log_method = logging.info
        elif status < 500:
            log_method = logging.warning
        else:
            log_method = logging.error
        request_time = 1000.0 * handler.request.request_time()
        if request_time > 30.0 or options.debug or status >= 400:
            log_method("%s %d %s %.2fms", options.port, status,
                       handler._request_summary(), request_time)


if __name__ == "__main__":
    # 当runmode为test的时候，把logging的级别设置为debug
    if options.runmode in ("test"):
        logging.info("set logging level to DEBUG")
        logging.getLogger().setLevel(logging.DEBUG)

    logging.info("listen port:%s", options.port)
    tornado.httpserver.HTTPServer(Application(), xheaders=True).listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
