# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def get_movements(self):
        domain = [('product_id', '=', self.id)]
        movements = self.env['stock.move'].search(domain)
        return movements

    @api.model
    def get_last_movement(self):
        domain = [('product_id', '=', self.id)]
        movement = self.env['stock.move'].search(domain, limit=1)
        return movement
