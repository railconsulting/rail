# -*- coding: utf-8 -*-
# Property of Rail Consulting. See LICENSE file for full copyright and licensing details.
{
    'name': 'Restricción de Almacen por Usuario | Restricción de Ubicaciones de Existencias',
    'version': '17.0.0.3',
    'category': 'Warehouse',
    'summary': 'Este módulo permite establecer según el usuario, los permisos de acceso a los almacenes y / o ubicaciones, así como sus operaciones',
    'description': """ 

        Warehouse Restriction for User in odoo,
        Configure Restriction in odoo,
        Operation Types Restriction in odoo,
        Warehouse Locations Restriction in odoo,
        Warehouse Restriction in odoo,

    """,
    "author": "Rail Consulting",
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
