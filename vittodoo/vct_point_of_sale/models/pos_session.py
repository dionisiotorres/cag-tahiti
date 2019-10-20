# -*- coding: utf-8 -*-
from datetime import date
from dateutil import relativedelta
from odoo import models, fields, api, _


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.multi
    def generate_report(self):
        if not self.stop_at:
            self.stop_at = date.today()
        data = {'date_start': self.start_at, 'date_stop': self.stop_at, 'config_ids': []}
        print("DATA: " + str(data))
        return self.env.ref('point_of_sale.sale_details_report').report_action([], data=data)
