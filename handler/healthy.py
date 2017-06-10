#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
healthy
"""
from lib.ecode import ECode
from handler.base import BaseHandler


class HealthyHandler(BaseHandler):
    """
    Solo Go service status health handler
    """
    def index(self):
        """
        """
        self.write("Good!")
