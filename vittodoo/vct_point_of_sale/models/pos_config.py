# -*- coding: utf-8 -*-

'''
Created on 1 mars 2017

@author: heifara
'''
from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    receipt_print_user = fields.Boolean(string="Imprimer le nom de l'utilisateur", help="Imprime le nom de l'utilisateur sur le reçu")
