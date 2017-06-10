#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
健康体检
"""
import requests
from lib.singleton import Singleton
default_ding_url = "https://oapi.dingtalk.com/robot/send"

class DingDingService(Singleton):
    """
    丁丁服务
    """
    def __init__(self, oapi=default_ding_url):
        """
        初始化
        """
        self.oapi=oapi

    def notify_text(self, text):
        """
        """
        pass

