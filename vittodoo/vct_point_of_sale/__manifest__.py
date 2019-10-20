# -*- coding: utf-8 -*-
{
    'name': "Point of Sale",

    'summary': """
    """,

    'description': """
    """,

    'author': "Vittoria Conseil",
    'website': "http://www.vittoriaconseil.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Point Of Sale',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        # data

        # views
        'views/pos_config_views.xml',
        'views/pos_session_view.xml',
    ],

    'qweb': [
        'static/src/xml/pos.xml',
    ],
    # only loaded in demonstration mode
}