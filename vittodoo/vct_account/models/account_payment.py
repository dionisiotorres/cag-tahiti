# -*- coding: utf-8 -*-

from odoo import models, fields, api


class account_payment(models.Model):
    _inherit = "account.payment"

    @api.model
    def default_get(self, fields):
        rec = super(account_payment, self).default_get(fields)
        invoice_defaults = self.resolve_2many_commands('invoice_ids', rec.get('invoice_ids'))
        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]
            rec['doc_number'] = invoice['reference'] or invoice['name'] or invoice['number']
            rec['comment'] = ""
        return rec

    doc_number = fields.Char(string="#")
    comment = fields.Char(string="Note")

    @api.onchange('doc_number', 'comment')
    def update_communication(self):
        if self.doc_number and self.comment:
            self.communication = self.doc_number + " " + self.comment
        elif self.doc_number:
            self.communication = self.doc_number
        elif self.comment:
            self.communication = self.comment
