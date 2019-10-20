# -*- coding: utf-8 -*-
{
    'name': "Gestion de stock par Vittoria Conseil",

    'summary': """
    """,

    'description': """
    """,

    'author': "Vittoria Conseil",
    'website': "http://www.vittoriaconseil.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Entrepôt',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        # views
        'views/stock_account_views.xml',
    ],

}
