# -*- coding: utf-8 -*-

'''
Created on 27 janv. 2017

@author: Heifara MATAPO
'''

from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    notahiti = fields.Char(string='N°Tahiti')