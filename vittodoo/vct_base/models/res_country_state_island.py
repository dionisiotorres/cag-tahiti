# -*- coding: utf-8 -*-
'''
Created on 19 janv. 2017

@author: Heifara MATAPO
'''

from odoo import models, fields

class Island(models.Model):
    _name = 'res.country.state.island'
    
    code = fields.Char('Code', required=True)
    name = fields.Char('Nom', required=True)
    state = fields.Many2one('res.country.state', required=True)
