# -*- coding: utf-8 -*-
{
    'name': 'Custom Products and Partners',

    'summary': "Data-only module with custom consumable product and partner",

    'description': """
This module provides a custom consumable product and a custom partner for Take Off assignment. It is designed to demonstrate the creation and management of products and partners using Odoo's data files.
    """,

    'author': "Sayed Mohamed Ebrahim",
    'website': "https://www.sayedmohd.com",

    'category': 'Sales',
    'version': '0.1',

    'depends': ['base', 'product','sale_management','purchase'],

    'data': [
        'data/attributes.xml',
        'data/products.xml',
        'data/partners.xml',
    ],

    'license': 'LGPL-3',

    'installable': True,
    'application': False,
    'auto_install': False,
}

