#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基础配置
"""
import os
import json
import logging

#  全局常量配置
HTTP_TIMEOUT = 3  # HTTP超时
LOG_HOME = "/tmp"  # 日志主目录
TMP_HOME = "/tmp"  # 临时路径

# 测试、灰度、线上
from tornado.options import define, options

if not hasattr(options, "runmode"):
    define("runmode", default="test", help="test prod")
    define("debug", default=True, help="enable debug")
    options.parse_command_line()

# 获取模板目录
parent_dir = os.path.dirname(os.path.realpath(__file__))
TPL_HOME = os.path.join(os.path.split(parent_dir)[0], "tpl")

# 加载相应环境的配置
if options.runmode == "test":
    from conf.settings_test import *

    logging.basicConfig(level=logging.DEBUG)

elif options.runmode == "prod":
    from conf.settings_prod import *

else:
    raise Exception("wrong runmode")

# 尝试从 local 配置中加载(一般用于覆盖上面引入的配置)
try:
    from conf.settings_local import *
except ImportError:
    pass
