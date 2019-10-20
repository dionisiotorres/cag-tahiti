# -*- coding: utf-8 -*-

import logging

from datetime import datetime, timedelta

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    invoice_id = fields.Many2one('account.invoice', 'Invoice')


class StockMove(models.Model):
    _inherit = "stock.move"

    invoice_line_ids = fields.Many2one('account.invoice.line', 'Invoice Line')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    invoice_id = fields.Many2one(related="group_id.invoice_id", string="Invoice", store=True)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def _default_warehouse_id(self):
        company = self.env.user.company_id.id
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company)], limit=1)
        return warehouse_ids

    @api.model
    def _default_picking_type(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)])
        if not types:
            types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return types[:1]

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To', states=READONLY_STATES, required=True, default=_default_picking_type, \
                                      help="This will determine operation type of incoming shipment")
    picking_policy = fields.Selection([
        ('direct', 'Deliver each product when available'),
        ('one', 'Deliver all products at once')],
        string='Shipping Policy', required=True, readonly=True, default='direct',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        default=_default_warehouse_id)

    picking_ids = fields.One2many('stock.picking', 'invoice_id', string='Pickings')
    picking_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')
    procurement_group_id = fields.Many2one('procurement.group', 'Procurement Group', copy=False)

    @api.depends('picking_ids')
    def _compute_picking_ids(self):
        for invoice in self:
            invoice.picking_count = len(invoice.picking_ids)

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()

        for invoice in self:
            if not invoice.picking_ids:
                sale_order = self._get_sale_order(invoice)
                if sale_order:
                    invoice.picking_ids = self.env['stock.picking'].search([('group_id', '=', sale_order.procurement_group_id.id)]) if sale_order.procurement_group_id else []

        for invoice in self:
            if not invoice.picking_ids:
                invoice.action_launch_procurement_rule()

        return res

    def _get_sale_order(self, invoice):
        '''
        Return the SaleOrder matching this invoice
        :param invoice: the invoice
        :return: The SaleOrder matching this invoice
        '''
        read_group = self.env['sale.order.line'].read_group([('invoice_lines', 'in', invoice.invoice_line_ids.ids)], ['order_id'], ['order_id'])
        order_id = [data['order_id'][0] for data in read_group]
        if len(order_id) > 0:
            order = self.env['sale.order'].browse([order_id[0]])
            return order
        else:
            return False

    @api.multi
    def action_view_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        pickings = self.mapped('picking_ids')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = pickings.id
        return action

    @api.multi
    def action_launch_procurement_rule(self):
        for invoice in self:
            if invoice.type in ('out_invoice'):
                invoice.invoice_line_ids._action_launch_procurement_rule()
            elif invoice.type in ('in_invoice'):
                invoice._create_picking()
            elif invoice.type in ('in_refund', 'out_refund'):
                _logger.warn('aucune opération à faire.')
            else:
                raise UserError(_('Aucune opération ne correspond à ce type de facture'))

    @api.multi
    def _create_picking(self):
        StockPicking = self.env['stock.picking']
        for invoice in self:
            if any([ptype in ['product', 'consu'] for ptype in invoice.invoice_line_ids.mapped('product_id.type')]):
                pickings = invoice.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
                if not pickings:
                    res = invoice._prepare_picking()
                    picking = StockPicking.create(res)
                else:
                    picking = pickings[0]
                moves = invoice.invoice_line_ids._create_stock_moves(picking)
                moves = moves.filtered(lambda x: x.state not in ('done', 'cancel'))._action_confirm()
                seq = 0
                for move in sorted(moves, key=lambda move: move.date_expected):
                    seq += 5
                    move.sequence = seq
                    moves._action_assign()
                    # picking.message_post_with_view('mail.message_origin_link', values={'self': picking, 'origin': order}, subtype_id=self.env.ref('mail.mt_note').id)
        return True

    @api.model
    def _prepare_picking(self):
        if not self.procurement_group_id:
            self.procurement_group_id = self.procurement_group_id.create({
                'name': self.number,
                'partner_id': self.partner_id.id,
                'invoice_id': self.id,
            })
        if not self.partner_id.property_stock_supplier.id:
            raise UserError(_("You must set a Vendor Location for this partner %s") % self.partner_id.name)
        return {
            'invoice_id': self.id,
            'picking_type_id': self.picking_type_id.id,
            'partner_id': self.partner_id.id,
            'date': self.date,
            'origin': self.name,
            'location_dest_id': self._get_destination_location(),
            'location_id': self.partner_id.property_stock_supplier.id,
            'company_id': self.company_id.id,
        }

    @api.multi
    def _get_destination_location(self):
        self.ensure_one()
        return self.picking_type_id.default_location_dest_id.id


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    route_id = fields.Many2one('stock.location.route', string='Route', domain=[('sale_selectable', '=', True)], ondelete='restrict')
    move_ids = fields.One2many('stock.move', 'invoice_line_ids', string='Stock Moves')

    @api.multi
    def _action_launch_procurement_rule(self):
        """
        Launch procurement group run method with required/custom fields genrated by a
        account invoice line. procurement group will launch '_run_move', '_run_buy' or '_run_manufacture'
        depending on the account invoice line product rule.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        errors = []
        for line in self:
            if not line.product_id:
                continue

            qty = 0.0
            for move in line.move_ids.filtered(lambda r: r.state != 'cancel'):
                qty += move.product_qty
            if float_compare(qty, line.quantity, precision_digits=precision) >= 0:
                continue

            group_id = line.invoice_id.procurement_group_id
            if not group_id:
                group_id = self.env['procurement.group'].create({
                    'name': line.invoice_id.number,
                    'move_type': line.invoice_id.picking_policy,
                    'invoice_id': line.invoice_id.id,
                    'partner_id': line.invoice_id.partner_id.id,
                })
                line.invoice_id.procurement_group_id = group_id
            else:
                # In case the procurement group is already created and the order was
                # cancelled, we need to update certain values of the group.
                updated_vals = {}
                if group_id.partner_id != line.invoice_id.partner_id.id:
                    updated_vals.update({'partner_id': line.invoice_id.partner_id.id})
                if group_id.move_type != line.invoice_id.picking_policy:
                    updated_vals.update({'move_type': line.invoice_id.picking_policy})
                if updated_vals:
                    group_id.write(updated_vals)

            values = line._prepare_procurement_values(group_id=group_id)
            product_qty = line.quantity - qty
            try:
                self.env['procurement.group'].run(line.product_id, product_qty, line.uom_id, line.invoice_id.partner_id.property_stock_customer, line.name, line.invoice_id.number, values)
            except UserError as error:
                errors.append(error.name)
        if errors:
            raise UserError('\n'.join(errors))
        return True

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        """ Prepare specific key for moves or other components that will be created from a procurement rule
        comming from a sale order line. This method could be override in order to add other custom key that could
        be used in move/po creation.
        """
        values = {}
        self.ensure_one()
        date_planned = datetime.strptime(self.invoice_id.date + " 00:00:00", DEFAULT_SERVER_DATETIME_FORMAT) \
                       + timedelta(days=self.product_id.sale_delay or 0.0) - timedelta(days=0.0)
        values.update({
            'company_id': self.invoice_id.company_id,
            'group_id': group_id,
            'date_planned': date_planned.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'route_ids': self.route_id,
            'warehouse_id': self.invoice_id.warehouse_id or False,
            'partner_dest_id': self.invoice_id.partner_id.id
        })
        return values

    @api.multi
    def _create_stock_moves(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            for val in line._prepare_stock_moves(picking):
                done += moves.create(val)
        return done

    @api.multi
    def _prepare_stock_moves(self, picking):
        """ Prepare the stock moves data for one order line. This function returns a list of
        dictionary ready to be used in stock.move's create()
        """
        self.ensure_one()
        res = []
        if self.product_id.type not in ['product', 'consu']:
            return res
        qty = 0.0
        price_unit = self._get_stock_move_price_unit()
        for move in self.move_ids.filtered(lambda x: x.state != 'cancel' and not x.location_dest_id.usage == "supplier"):
            qty += move.product_qty
        template = {
            'name': self.name or '',
            'product_id': self.product_id.id,
            'product_uom': self.uom_id.id,
            'date': self.invoice_id.date,
            'date_expected': self.invoice_id.date,
            'location_id': self.invoice_id.partner_id.property_stock_supplier.id,
            'location_dest_id': self.invoice_id._get_destination_location(),
            'picking_id': picking.id,
            'partner_id': self.invoice_id.partner_id.id,
            'move_dest_ids': [(4, x) for x in self.move_ids.ids],
            'state': 'draft',
            'invoice_line_ids': self.id,
            'company_id': self.invoice_id.company_id.id,
            'price_unit': price_unit,
            'picking_type_id': self.invoice_id.picking_type_id.id,
            'group_id': self.invoice_id.procurement_group_id.id,
            'origin': self.invoice_id.number,
            'route_ids': self.invoice_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.invoice_id.picking_type_id.warehouse_id.route_ids])] or [],
            'warehouse_id': self.invoice_id.picking_type_id.warehouse_id.id,
        }
        diff_quantity = self.quantity - qty
        if float_compare(diff_quantity, 0.0, precision_rounding=self.uom_id.rounding) > 0:
            template['product_uom_qty'] = diff_quantity
            res.append(template)
        return res

    @api.multi
    def _get_stock_move_price_unit(self):
        self.ensure_one()
        line = self[0]
        invoice = line.invoice_id
        price_unit = line.price_unit
        if line.invoice_line_tax_ids:
            price_unit = line.invoice_line_tax_ids.with_context(round=False).compute_all(
                price_unit, currency=line.invoice_id.currency_id, quantity=1.0, product=line.product_id, partner=line.invoice_id.partner_id
            )['total_excluded']
        if line.uom_id != line.product_id.uom_id.id:
            price_unit *= line.uom_id.factor / line.product_id.uom_id.factor
        if invoice.currency_id != invoice.company_id.currency_id:
            price_unit = invoice.currency_id.compute(price_unit, invoice.company_id.currency_id, round=False)
        return price_unit
