# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Sale(models.Model):
    _inherit = "sale.order"

    def default_sellers(self):
        return [self.env.user.id]

    sellers = fields.Many2many('res.users', string='Vendeurs', index=True, default=default_sellers)

    @api.multi
    def _prepare_invoice(self):
        res = super(Sale, self)._prepare_invoice()
        res['sellers'] = [(4, seller.id, False) for seller in self.sellers]
        return res
