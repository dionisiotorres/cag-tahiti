# -*- coding: utf-8 -*-

'''
Created on 28 avr. 2017

@author: Heifara MATAPO
'''

from odoo import fields, models, api

class HrPayrollConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    compute_leaves = fields.Boolean(string='Calculer les jours de congés', help="Create journal entries from payslips")

    @api.multi
    def set_compute_leaves(self):
        self.ensure_one()
        self.env['ir.config_parameter'].set_param('vct_hr_payroll.compute_leaves', self.compute_leaves)
    
    @api.model
    def get_default_compute_leaves(self, fields):
        return {
            'compute_leaves': self.env['ir.config_parameter'].get_param('vct_hr_payroll.compute_leaves'),
        }
