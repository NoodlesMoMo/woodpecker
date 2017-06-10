#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化相关表
"""
import os
import sys
from tornado.options import define, options

define('cmd', default='initable', help='命令')

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))
from model.inspect.project import (InspectProjectModel, InspectObjectModel,
                                   InspectTargetModel, InspectItemModel)
from model.inspect.task import (InspectTaskModel, InspectItemResultModel,
                                InspectScoreResultModel)
from model.purchase.enquiry import EnquiryModel
from model.purchase.pricing import PricingModel, PricingDetailModel, PricingMaterielModel
from model.purchase.purchase import PurchaseOrderModel, PurchaseMaterielModel
from model.purchase.requisition import (ApplyOrderModel, ApplyDetailModel,
                                        OrderSummaryModel, OrderApplyRelModel,
                                        OrderMaterielModel)
from model.purchase.supplier import SupplierModel
from model.warehouse.canteen import CanteenModel, PartitionModel, StallModel
from model.warehouse.materiel import MaterielTypeModel, MaterielModel
from model.warehouse.stock import (StockModel, StockChangeModel, StockInventoryModel,
                                   InventoryDetailModel, WarehousingEntryModel,
                                   EntryDetailModel, DeliveryOrderModel,
                                   DeliveryDetailModel)
from model.warehouse.team import TeamModel, SettleHistoryModel
from model.warehouse.warehouse import WarehouseModel
from model.stat.finance import (TeamIncomeModel, TeamIncomeDetailModel, TeamFeeModel,
                                TeamFeeDetailModel, TeamMaterielStatModel,
                                TeamMaterielDetailModel, TeamBusinessModel)
from model.stat.policy import (InventoryMonthReportModel, PurchaseMonthReportModel,
                               PurchaseDetailModel, MaterielAnalysisModel)
from model.common.setting import CommonSettingModel


class BootStrap(object):
    """
    initing
    """

    def init_table(self):
        """
        创建相关数据库表
        """
        # 巡检
        for i in (InspectProjectModel, InspectObjectModel, InspectTargetModel,
                  InspectTaskModel, InspectItemModel, InspectItemResultModel,
                  InspectScoreResultModel):
            i.new().init_table()

        # 采购
        for i in (EnquiryModel, PricingModel, PricingDetailModel, PricingMaterielModel,
                  PurchaseOrderModel, PurchaseMaterielModel,
                  ApplyOrderModel, ApplyDetailModel, OrderSummaryModel, SupplierModel,
                  OrderApplyRelModel, OrderMaterielModel):
            i.new().init_table()

        # 仓库
        for i in (CanteenModel, MaterielTypeModel, MaterielModel, DeliveryDetailModel,
                  DeliveryOrderModel, EntryDetailModel, InventoryDetailModel,
                  StockChangeModel, StockInventoryModel, StockModel, TeamModel,
                  WarehousingEntryModel, SettleHistoryModel, WarehouseModel,
                  PartitionModel, StallModel):
            i.new().init_table()

        # 统计
        for i in (TeamBusinessModel, TeamFeeModel, TeamMaterielStatModel, TeamIncomeModel,
                  InventoryDetailModel, InventoryMonthReportModel, PurchaseDetailModel,
                  MaterielAnalysisModel, PurchaseMonthReportModel, TeamFeeDetailModel,
                  TeamMaterielDetailModel, TeamIncomeDetailModel):
            i.new().init_table()

        # 通用
        for i in (CommonSettingModel,):
            i.new().init_table()


if __name__ == '__main__':
    cmd = options.cmd

    BS = BootStrap()

    if cmd == "initable":
        BS.init_table()

