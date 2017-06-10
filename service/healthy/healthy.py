#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
健康体检
"""
from lib.singleton import Singleton


class HealthyService(Singleton):
    """
    体检服务
    """
    def __init__(self):
        """
        初始化
        """
        pass

    def ding_notify(self, params):
        """
        添加仓库
        :param params: {
                "campus_id": 学校id,
                "zone_id": 校区id,
                "name": 名称,
                "address": 地址,
                "mgr_org_id": 管理部门id,
                "pur_org_id": 采购部门id,
                "create_user": 创建人,
                "update_user": 更新人
            }
        :return: code, healthy
        """
        pass
