# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    nbr_reordering_rules = fields.Integer('Reordering Rules', compute='_compute_nbr_reordering_rules')

    def _compute_nbr_reordering_rules(self):
        ids = []
        for ol in self.order_line:
            for op in ol.orderpoint_id:
                ids.append(op.id)
        self.nbr_reordering_rules = len(ids)

    @api.multi
    def action_view_reordering_rule(self):
        ids = []
        for ol in self.order_line:
            for op in ol.orderpoint_id:
                ids.append(op.id)

        return {
            'domain': "[('id', 'in', " + str(ids) + ")]",
            'type': 'ir.actions.act_window',
            'res_model': 'stock.warehouse.orderpoint',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_id': [int(id) for id in ids]
        }
