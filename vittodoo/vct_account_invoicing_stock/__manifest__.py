# -*- coding: utf-8 -*-
{
    'name': "Facture et stock",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Vittoria Conseil",
    'website': "https://vittoriaconseil.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Invoicing Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'account_invoicing'],

    # always loaded
    'data': [
        'views/account_invoice_view.xml',
    ],
}