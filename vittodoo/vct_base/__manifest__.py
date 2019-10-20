# -*- coding: utf-8 -*-
{
    'name': "Base Vittoria Conseil",

    'summary': """
    """,

    'description': """
    """,

    'author': "Vittoria Conseil",
    'website': "http://www.vittoriaconseil.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sample',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'l10n_fr', 'account_invoicing', 'contacts', 'crm'],

    # always loaded
    'data': [
        # data
        'data/res.bank.csv',
        'data/res.company_data.xml',
        'data/res.country.state.csv',
        'data/res.country.state.island.csv',
        'data/res.currency.csv',
        'data/res.partner.category.csv',
        'data/resource.xml',
        
        # views
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
    ],
    
    'qweb': [
        "static/src/xml/*.xml",
    ],
}
