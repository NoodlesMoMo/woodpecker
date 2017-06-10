#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全局配置业务错误码
"""
from enum import Enum, EnumMem


class ECode(Enum):
    """
    错误码
    """
    # 系统码
    SUCC = EnumMem(0, "SUCC")
    PARAM = EnumMem(1, "参数错误")
    INTER = EnumMem(2, "内部错误")
    TIMEOUT = EnumMem(3, "外部接口超时")
    EXTERNAL = EnumMem(4, "外部接口错误")
    RESRC = EnumMem(5, "接口不存在")
    AUTH = EnumMem(6, "鉴权失败")
    FORBID = EnumMem(7, "访问禁止")
