# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = "res.partner"

    _sql_constraints = [
        ('check_name', "CHECK(1=1)", 'Contacts require a name.'),
    ]
