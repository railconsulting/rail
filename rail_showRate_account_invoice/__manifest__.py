# -*- coding: utf-8 -*-
{
    'name': "Rail Show Currency Rate for Invoices",

    'summary': """
        A customization to show in the invoice form the currency rate if the currency in transaction is 
        different with the company currency""",

    'author': "Rail / Ernesto Diaz",
    'website': "https://rail.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '1.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'views/account_move.xml',
    ],
    'license': 'LGPL-3',
}
