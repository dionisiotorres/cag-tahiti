# -*- coding: utf-8 -*-

'''
Created on 30 mars 2017

@author: heifara
'''

from odoo import models, fields, api
from odoo.tools.translate import _

class HolidaysType(models.Model):
    _inherit = "hr.holidays.status"

    count = fields.Boolean('Active le comptage des jours de congés malgré le dépassement de limite autorisé')
    
    @api.onchange('limit')
    def onchange_limit(self):
        if self.limit == False:
            self.count = True
        elif self.limit:
            self.count = False
            

    @api.multi
    def name_get(self):
        if not self._context.get('employee_id'):
            # leave counts is based on employee_id, would be inaccurate if not based on correct employee
            return super(HolidaysType, self).name_get()
        res = []
        for record in self:
            name = record.name
            if record.count:
                name = "%(name)s (%(count)s)" % {
                    'name': name,
                    'count': _('%g remaining out of %g') % (record.virtual_remaining_leaves or 0.0, record.max_leaves or 0.0)
                }
            res.append((record.id, name))
        return res
