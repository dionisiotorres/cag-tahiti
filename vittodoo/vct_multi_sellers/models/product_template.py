from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    exclude_from_base_commission = fields.Boolean(string="Exclure de la base commissionnable")
