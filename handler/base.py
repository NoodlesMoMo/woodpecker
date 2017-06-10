#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handler基类
"""
import json
import pprint
import logging
import decimal
import datetime
import tornado.web
from tornado.options import options
from conf.settings import LOG_HOME
from lib.utils import json_dumps, json_default, write2log
from lib.ecode import ECode


class InnerException(Exception):
    """
    mweb exception
    """
    pass


class ParamException(Exception):
    """
    参数异常
    """
    code, msg = ECode.PARAM, None

    def __init__(self, msg, *args, **kwargs):
        """
        初始化
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        super(ParamException, self).__init__(*args, **kwargs)
        self.msg = msg


class BaseHandler(tornado.web.RequestHandler):
    """
    基础类
    """
    ARG_DEFAULT = object()
    TORNADO_ARG_DEFAULT = tornado.web.RequestHandler._ARG_DEFAULT

    def get_argument(self, name, default=TORNADO_ARG_DEFAULT, strip=True):
        """
        重写以把unicode的参数都进行utf-8编码
        :param string name: 字段名字
        :param dict default: 转换格式
        :param bool strip: 去掉前后空白
        :return:
        """
        value = super(BaseHandler, self).get_argument(name, default, strip)
        if isinstance(value, unicode):
            value = value.encode("utf-8")
        return value

    def get_argument_int(self, name, default=ARG_DEFAULT):
        """
        获取整型参数
        :param string name: 参数名
        :param list default: 如果未传此参数时得到的默认值
        :return: 返回得到的整型值
        """
        value = self.get_argument(name, default)
        if value == self.ARG_DEFAULT:
            raise ParamException("参数: %s 不能为空" % name)
        elif value == default:
            return value
        try:
            value = int(value)
        except:
            if default != self.ARG_DEFAULT:
                return default
            raise ParamException("参数: %s 格式不正确" % name)
        return value

    def get_argument_float(self, name, default=ARG_DEFAULT):
        """
        获取浮点型
        :param string name: 名字
        :param list default:
        :return:
        """
        value = self.get_argument(name, default)
        if value == self.ARG_DEFAULT:
            raise ParamException("参数: %s 不能为空" % name)
        elif value == default:
            return value
        try:
            value = float(value)
        except ValueError:
            if default != self.ARG_DEFAULT:
                return default
            raise ParamException("参数: %s 格式不正确" % name)
        return value

    def get_argument_datetime(self, name, default=ARG_DEFAULT):
        """
        获取时间
        :param name:
        :param default:
        :return:
        """
        value = self.get_argument(name, default)
        if value == self.ARG_DEFAULT:
            raise ParamException("参数: %s 不能为空" % name)
        elif value == default:
            return value

        try:
            value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            if default != self.ARG_DEFAULT:
                return default
            raise ParamException("参数: %s 格式不正确" % name)
        return value

    def get_argument_date(self, name, default=ARG_DEFAULT):
        """
        获取日期
        :param name:
        :param default:
        :return:
        """
        value = self.get_argument(name, default)
        if value == self.ARG_DEFAULT:
            raise ParamException("参数: %s 不能为空" % name)
        elif value == default:
            return value

        try:
            value = datetime.datetime.strptime(value, "%Y-%m-%d")
            value = value.date()
        except ValueError:
            if default != self.ARG_DEFAULT:
                return default
            raise ParamException("参数: %s 格式不正确" % name)
        return value

    def get_argument_decimal(self, name, default=ARG_DEFAULT):
        """
        最大参数
        :param name:
        :param default:
        :return:
        """
        value = self.get_argument(name, default)
        if value == self.ARG_DEFAULT:
            raise ParamException("参数: %s 不能为空" % name)
        elif value == default:
            return value

        try:
            value = decimal.Decimal(value)
        except ValueError:
            if default != self.ARG_DEFAULT:
                return default
            raise ParamException("参数: %s 格式不正确" % name)
        return value

    def send_json(self, res, code=ECode.SUCC, msg=None):
        """
        发送json数据
        """
        response = {
            "code": code,
            "msg": msg or ECode.dict().get(code, None),
            "body": res
        }

        # 当响应为失败或者当前的debug模式为真的情况下,显示请求和响应信息
        if code != ECode.SUCC:
            logging.warn("request: %s", self.request.arguments)
            logging.error("response fail: %s", json_dumps(response))
        elif options.debug:
            logging.warn("request: %s", self.request.arguments)

            # 对于非常大的数据, 用pprint的depth参数, 能自动的忽略更深深度的数据
            response_str = json_dumps(response, indent=2)
            if len(response_str) <= 2048:
                logging.warn("response succ: \n%s", response_str)
            else:
                logging.warn("response succ: \n%s",
                             pprint.pformat(response, width=1, indent=2, depth=2))

        self.finish(json.dumps(response, default=json_default))

    def get_current_user(self):
        """
        Tornado的回调函数, 获取当前用户
        """
        # TODO user info
        user = {
            "id": 1,
            "name": "测试",
        }
        return user

    def process_module(self, module):
        """
        内部路由分发
        """
        module = "__".join([i for i in (module or "").split("/") if i])
        method = getattr(self, module or "index", None)
        if method:
            try:
                if options.debug:
                    logging.info("request: %s", self.request.arguments)
                method()
            except ParamException, msg:
                logging.error("%s\n%s\n", self.request, str(msg), exc_info=True)
                self.send_json(None, ECode.PARAM, str(msg))
            except RuntimeError, msg:
                logging.error("%s\n%s\n", self.request, str(msg), exc_info=True)
                self.send_json(None, ECode.TIMEOUT, str(msg))
            except AttributeError, msg:
                logging.error("%s\n%s\n", self.request, str(msg), exc_info=True)
                self.send_json(None, ECode.RESRC, str(msg))
            except Exception, msg:
                logging.error("%s\n%s\n", self.request, str(msg), exc_info=True)
                msg = None if options.runmode == "prod" else str(msg)
                self.send_json(None, ECode.INTER, msg)
        else:
            raise tornado.web.HTTPError(404)

    def get(self, module):
        """
        HTTP GET处理
        """
        self.process_module(module)

    def post(self, module):
        """
        HTTP POST处理
        """
        if not self.request.files:
            write2log(LOG_HOME, "post_swan",
                      self.request.uri, self.request.body)
        self.process_module(module)

    def data_received(self, chunk):
        """
        数据
        """
        pass

    def send_file(self, name, data, mime_type="application/octet-stream"):
        """
        发送文件
        :param name: 文件名
        :param data: 文件数据, bytes/unicode
        :param mime_type: 文件类型, 默认 "application/octet-stream"
        """
        # 设置 header
        self.set_header("Content-Disposition", "attachment; filename=" + name)
        self.set_header("Content-Type", mime_type)

        # 不缓存
        self.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.set_header("Pragma", "no-cache")
        self.set_header("Expires", "0")

        self.write(data)
        self.finish()

