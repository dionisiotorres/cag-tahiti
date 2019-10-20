# -*- coding: utf-8 -*-

'''
Created on 19 janv. 2017

@author: Heifara MATAPO
'''
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ref = fields.Char(string='Internal Reference', index=True, store=True)

    last_name = fields.Char('Nom de famille')
    first_name = fields.Char('Prénom')
    second_name = fields.Char('Deuxième Prénom')

    island = fields.Many2one('res.country.state.island')
    trade_name = fields.Char('Nom Commercial', help='Nom Commercial')

    lock = fields.Boolean("Verrouiller")
    lock_date = fields.Datetime("Date de verrou")
    lock_text = fields.Char(compute="compute_lock_text")

    archive = fields.Boolean("Archiver")
    archive_date = fields.Datetime("Date d'archive")

    birth_date = fields.Date("Date d'anniversaire")

    @api.onchange('last_name', 'first_name', 'second_name')
    def update_name(self):
        for item in self:
            if item.last_name and item.first_name:
                item.name = item.last_name + " " + item.first_name
            elif item.first_name:
                item.name = item.first_name
            elif item.last_name:
                item.name = item.last_name

    @api.onchange('last_name', 'first_name', 'second_name')
    def update_ref_onchange(self):
        if not self.ref:
            if self.last_name and self.first_name:
                self.ref = self.last_name + self.first_name.upper()[0:4]

    @api.onchange('island')
    def onchange_island(self):
        if self.island:
            self.state_id = self.island.state.id

    @api.onchange('state_id')
    def onchange_state(self):
        res = {'domain': {'state_id': [], 'island': []}}
        if self.state_id:
            ids = self.state_id.mapped("id")
            res['domain'] = {
                'island': [('state', 'in', ids)],
            }
            self.country_id = self.state_id.country_id
            if self.island.state.id not in ids:
                self.island = None
        else:
            self.island = None

        return res

    @api.onchange('country_id')
    def onchange_country(self):
        res = {'domain': {'state_id': [], 'island': []}}
        if self.country_id:
            ids = self.country_id.mapped("id")
            res['domain'] = {
                'state_id': [('country_id', 'in', ids)],
            }
            if self.state_id.country_id.id not in ids:
                self.state_id = None
                self.island = None

        return res

    @api.onchange('lock')
    def onchange_lock(self):
        self.lock_date = fields.Datetime().now()

    @api.multi
    def toggle_active(self):
        super(ResPartner, self).toggle_active()
        for record in self:
            record.write({'archive': not record.active})
            record.write({'archive_date': fields.Datetime.now()})

    @api.depends('lock', 'lock_date')
    def compute_lock_text(self):
        for item in self:
            if item.lock and item.lock_date:
                item.lock_text = "Attention !! Ce client à été verrouillé le " + item.lock_date
            elif item.lock_date:
                item.lock_text = "Attention !! Ce client à été verrouillé le " + item.lock_date
