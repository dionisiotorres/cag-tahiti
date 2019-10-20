# -*- coding: utf-8 -*-

'''
Created on 24 juin 2017

@author: heifara
'''

from odoo import models, fields, api

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    billed_amount = fields.Float()
    invoice = fields.Many2one(comodel_name='account.invoice', string='Facture')
    
    # @override AccountAnalyticLine.create(self, vals)
    # @see hr_timesheet.hr_timesheet: AccountAnalyticLine
    @api.model
    def create(self, vals):
        if vals.get('account_id'):
            selected_account_id = vals['account_id']
            result = super(AccountAnalyticLine, self).create(vals)
            result.write({'account_id': selected_account_id})        
            return result
        else:
            return super(AccountAnalyticLine, self).create(vals)