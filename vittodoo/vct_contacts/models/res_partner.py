# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_partner(models.Model):
    _inherit = 'res.partner'

    activity = fields.Char()
    effectif = fields.Char()
    multi_site = fields.Integer(default=1)
    internet_apps = fields.Char()
    intranet_ged_apps = fields.Char()
    erp_apps = fields.Char()
    hosting = fields.Selection(selection=[
        ('cloud', 'Cloud'),
        ('server', 'Serveur')
    ], default='cloud')
    security_apps = fields.Char()
    mdm = fields.Boolean()
