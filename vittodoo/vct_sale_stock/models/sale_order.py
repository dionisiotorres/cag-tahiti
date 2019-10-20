# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    def _onchange_product_id_check_availability(self):
        '''
        Disable return of warning messages.
        :return:
        '''
        # res = super(SaleOrderLine, self)._onchange_product_id_check_availability()
        return {}
