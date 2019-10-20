# -*- coding: utf-8 -*-
{
    'name': "Gestion des Congés",

    'summary': """
        Module complémentaire pour la gestion des congés.
    """,

    'description': """
        Module complémentaire pour la gestion des congés.
    """,

    'author': "Vittoria Conseil",
    'website': "http://www.vittoriaconseil.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Employés',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['vct_base', 'hr_holidays'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/hr_holidays_report.xml',
        'report/hr_holidays_templates.xml',
        
        'views/vct_hr_holidays_status.xml',
    ],
}