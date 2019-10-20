# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _gather(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False):
        wh = self.env['stock.warehouse'].search([('lot_stock_id','=',location_id.id)])
        if wh and wh.default_resupply_wh_id:
            return super(StockQuant, self)._gather(product_id, wh.default_resupply_wh_id.lot_stock_id, lot_id, package_id, owner_id, strict)
        else:
            return super(StockQuant, self)._gather(product_id, location_id, lot_id, package_id, owner_id, strict)
