# -*- coding: utf-8 -*-

'''
Created on 30 mars 2017

@author: heifara
'''

from odoo import models, api, fields

class Employee(models.Model):
    _inherit = "hr.employee"
    
    leaves_count = fields.Float('Number of Leaves', compute='_compute_leaves_count')

    @api.multi
    def _compute_leaves_count(self):
        leaves = self.env['hr.holidays'].read_group([
            ('employee_id', 'in', self.ids),
            ('holiday_status_id.count', '=', True),
            ('state', '=', 'validate')
        ], fields=['number_of_days', 'employee_id'], groupby=['employee_id'])
        mapping = dict([(leave['employee_id'][0], leave['number_of_days']) for leave in leaves])
        for employee in self:
            employee.leaves_count = mapping.get(employee.id)
