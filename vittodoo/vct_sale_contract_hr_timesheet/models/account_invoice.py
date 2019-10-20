# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    timesheets = fields.One2many(comodel_name='account.analytic.line', inverse_name='invoice', string='Feuilles de temps facturées')
