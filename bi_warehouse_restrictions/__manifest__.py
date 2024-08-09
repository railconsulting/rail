# -*- coding: utf-8 -*-
# Part of Rail Consulting apps. See LICENSE file for full copyright and licensing details.
{
    'name': 'User Warehouse Restriction | Stock Location Restriction',
    'version': '17.0.0.3',
    'category': 'Warehouse',
    'summary': 'User Warehouse Restriction Warehouse location restriction user restriction on warehouse location stock access control stock access rules stock restriction restrict warehouse restrict location operation restriction stock access rules warehouse access rules',
    'description': """ 

        Warehouse Restriction for User in odoo,
        Configure Restriction in odoo,
        Operation Types Restriction in odoo,
        Warehouse Locations Restriction in odoo,
        Warehouse Restriction in odoo,

    """,
    "author": "Rail Consulting",
    "price": 1600,
    "currency": 'MXN',
    "website" : "https://www.rail.com.mx",
    'depends': ['base', 'stock'],
    'data': [
            'security/restriction_rules.xml',
            'views/res_users_inherited.xml',
            ],
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "images":["static/description/Banner.gif"]
}
