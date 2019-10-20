# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoiceSellerCommission(models.Model):
    _name = 'account.invoice.seller.commission'
    _description = 'Répartition des commissions vendeurs'

    account_invoice = fields.Many2one('account.invoice', string='Facture')
    date = fields.Date(related='account_invoice.date_invoice', store=True)
    seller = fields.Many2one('res.users', string='Vendeur', index=True)
    commission = fields.Float(string='Base Commission vendeur', readonly=True)
