# -*- coding: utf-8 -*-
{
    'name': "Gestion des événement par Vittoria Conseil",

    'summary': """
    """,

    'description': """
    """,

    'author': "Vittoria Conseil",
    'website': "http://www.vittoriaconseil.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Marketing',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['website_event'],

    # always loaded
    'data': [
        'views/website_event_templates.xml',
    ],
}