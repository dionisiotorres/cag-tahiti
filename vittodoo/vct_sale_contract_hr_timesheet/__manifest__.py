# -*- coding: utf-8 -*-
{
    'name': "Subscription Management with Timesheet invoicing",

    'summary': """
    Créer des abonnements. A la génération de facture, certains produits sont facturés au réél, c'est-à-dire les temps notés sur les feuilles de temps.
    """,

    'description': """
    Scénario :
    1. Créer un article d'abonnement => [(Product Type: Service), (Invoice Policy : Delivered quantities), (Track Service : Create a task and track hours)]
    2. Créer un modèle d'abonnement avec cette article
    3. Créer un abonnement
    4. Commencer l'abonnement
    5. Ajouter une feuille de temps sur le compte analytic correspondant à l'abonnement. Ne pas oublié de cocher "Billable"
    6. Cliquer sur Générer une facture
    """,

    'author': "Vittoria Conseil",
    'website': "http://www.vittoriaconseil.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Ventes',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_subscription_asset', 'sale_subscription', 'hr_timesheet'],

    # always loaded
    'data': [
        'data/sale_subscription_data.xml',

        'views/sale_subscription_views.xml',
    ],
}
