# -*- coding: utf-8 -*-
{
    'name': "Paie en Polynésie Française",

    'summary': """
    Tous le nécessaire pour la gérer la paie en Polynésie Française.
    """,

    'description': """
    Tous le nécessaire pour la gérer la paie en Polynésie Française.
    """,

    'author': "Vittoria Conseil",
    'website': "http://www.vittoriaconseil.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Employés',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['vct_base', 'hr_payroll', 'hr_payroll_account','l10n_fr'],

    # always loaded
    'data': [
        'data/hr.salary.rule.category.csv',
        'data/hr.salary.rule.csv',
        'data/hr.payroll.structure.csv',
        
        'views/report_payslip_templates.xml',
        'views/hr_payroll_views.xml',
        'views/res_config_views.xml',
    ],
}