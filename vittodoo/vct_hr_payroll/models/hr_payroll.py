# -*- coding:utf-8 -*-

'''
Created on 28 avr. 2017

@author: Heifara MATAPO
'''
from odoo import api, fields, models

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    leaves_previous_month = fields.Float('Reliquat mois précédent')
    leaves_taken_month = fields.Float('Jours pris dans le mois')
    leaves_earned_month = fields.Float('Jours acquis dans le mois')
    leaves_count = fields.Float('Solde')
    alert_message = fields.Char("Attention!!! les jours de congés ont été recalculés")
    alert_message_shown = fields.Boolean()
    
    @api.multi
    def compute_sheet(self):
        if super(HrPayslip, self).compute_sheet():
            if self.env['ir.config_parameter'].get_param('vct_hr_payroll.compute_leaves'):
                self.compute_leaves_previous_month()
                self.compute_leaves_taken_month()
                self.compute_leaves_earned_month()
                self.leaves_count = self.employee_id.leaves_count
                self.alert_message_shown = True
            return True
        else:
            return False
        
    @api.onchange('leaves_previous_month', 'leaves_taken_month', 'leaves_earned_month', 'leaves_count')
    def hide_alert_message(self):
        self.alert_message_shown = False
        
    @api.multi
    def compute_leaves_previous_month(self):
        self.leaves_previous_month = 0;
        
    @api.multi
    def compute_leaves_taken_month(self):
        self.leaves_taken_month = 0;
        
    @api.multi
    def compute_leaves_earned_month(self):
        self.leaves_earned_month = 0;
    
