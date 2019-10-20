# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def default_sellers(self):
        return [self.env.user.id]

    sellers = fields.Many2many('res.users', string='Vendeurs', index=True, default=default_sellers, readonly=True, states={'draft': [('readonly', False)]})
    account_invoice_seller_commissions = fields.One2many(comodel_name='account.invoice.seller.commission', inverse_name='account_invoice', string='Répartition de la base commissionnable par vendeur', readonly=True)

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()
        self.calc_commission()
        return res

    @api.multi
    def action_cancel(self):
        res = super(AccountInvoice, self).action_cancel()
        if self.state == 'cancel':
            self.account_invoice_seller_commissions = False
        return res

    @api.onchange('state', 'sellers')
    def calc_commission(self):
        self.account_invoice_seller_commissions = False
        for seller in self.sellers:
            if self.id:
                vals = self._prepare_commission(seller)
                self.env['account.invoice.seller.commission'].create(vals)


    def _prepare_commission(self, seller):
        commission = 0

        for invoice_line in self.invoice_line_ids:
            if invoice_line.product_id.exclude_from_base_commission:
                continue
            else:
                commission = commission + invoice_line.price_subtotal

        # If refund then substract the commission
        if self.type in ('out_refund', 'in_refund'):
            commission *= -1
        # If canceled then commission is 0

        #print(str(commission)+" :"+str(self.state))
        #if self.state in ('cancel') and (commission>0):
        if self.state in ('cancel'):
            commission = 0

        vals = {
            'account_invoice': self.id,
            'seller': seller.id,
            #'commission': commission / len(self.sellers) if commission > 0 else 0,
            'commission': commission / len(self.sellers),
        }

        return vals
