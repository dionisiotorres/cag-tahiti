# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    partner_id = fields.Many2one(related='move_id.picking_partner_id')
