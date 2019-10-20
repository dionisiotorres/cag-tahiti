# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    picking_partner_id = fields.Many2one('res.partner', 'Transfer Destination Address', related='picking_id.partner_id', store=True)
    average_delivery = fields.Float(string="Consommation Moyenne", compute="_compute_average_delivery", store=True, group_operator='avg', readonly=True)

    @api.depends('product_qty')
    def _compute_average_delivery(self):
        for this in self:
            this.average_delivery = this.product_qty


class StockPicking(models.Model):
    _inherit = "stock.picking"

    partner_ref = fields.Char(string="Référence fournisseur")


class ProductProduct(models.Model):
    _inherit = "product.product"

    average_delivery = fields.Float(string="Consommation Moyenne sur les 6 derniers mois", compute="_compute_average_delivery")
    remaining_quantity = fields.Float(string="Attendu", help="Relicat de commandes fournisseurs", compute="_compute_remaining_quantity")
    frozen_consumption = fields.Float(string="Consommation figé", compute="_compute_frozen_consumption")

    def _compute_average_delivery(self):
        for this in self:
            domain = [('product_id.id', '=', this.id),
                      ('state', '=', 'done'),
                      ('picking_id.picking_type_id.code', '=', 'outgoing')]
            stock_move_lines = self.env['stock.move.line'].search(domain)
            average_delivery = 0.0
            for stock_move_line in stock_move_lines:
                # print("REF: " + str(stock_move_line.reference) + "PRODUCT: " + str(stock_move_line.product_id.display_name) + "QTE: " + str(stock_move_line.qty_done))
                average_delivery = average_delivery + stock_move_line.qty_done
            this.average_delivery = average_delivery / len(stock_move_lines) if average_delivery > 0 else 0.0

    def _compute_remaining_quantity(self):
        for this in self:
            domain = [('product_id.id', '=', this.id),
                      ('state', 'in', ('purchase', 'done'))]
            purchase_order_lines = self.env['purchase.order.line'].search(domain)
            remaining_quantity = 0.0
            for purchase_order_line in purchase_order_lines:
                print("REF: " + str(purchase_order_line.order_id.display_name) + "PRODUCT: " + str(purchase_order_line.product_id.display_name))
                remaining_quantity = remaining_quantity + (purchase_order_line.product_qty - purchase_order_line.qty_received)
            this.remaining_quantity = remaining_quantity

    def _compute_frozen_consumption(self):
        for this in self:
            this.frozen_consumption = this.orderpoint_ids.product_min_qty / 3
