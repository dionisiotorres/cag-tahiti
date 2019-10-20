# -*- coding: utf-8 -*-
{
    "name": """Sync restaurant orders across multiple sessions""",
    "summary": """Use multiple POS for handling restaurant orders""",
    "category": "Point of Sale",

    "author": "TechnoSquare",
    "support": "info@technosquare.in",
    "website": "http://technosquare.in/",

    "depends": [
        "bus",
        "pos_restaurant",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/templates.xml",
        "views/views.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "qweb": [
        "static/src/xml/pos_longpolling_connection.xml",
        "static/src/xml/sync_pos_orders.xml",
    ],
    'images': ['static/description/banner.jpg'],
    'live_test_url': 'https://youtu.be/jmD5gJX2tfE',
    'price': 149,
    'currency': "EUR",
    "auto_install": False,
    "installable": True,
}
