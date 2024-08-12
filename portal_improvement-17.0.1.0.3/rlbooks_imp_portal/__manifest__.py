# -*- coding: utf-8 -*-
# Copyright 2024 RL Software Development ApS. See LICENSE file for full copyright and licensing details.
{
    'name': "Portal improvements",

    'summary': """
        Extends the portal functionality.
    """,

    'description': """
            
    """,

    'author': "RL Software Development ApS",
    'website': "https://www.rlsd.dk/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Website',
    'version': '17.0.1.0.3',

    # any module necessary for this one to work correctly
    'depends': [
        'portal',
        'web',
        'base'
    ],

    # always loaded
    'data': [
        'views/portal_my_home.xml',             
    ],
    'css': [
        'static/src/css/portal_my_home.css',
    ],
    # 'assets': {
    #     'web.assets_frontend': [            
    #     ],
    # },
    'price': 0.0,
    'currency': 'EUR',
    'support': 'support@rlsd.dk',
    # 'live_test_url': '',
    "images":[        
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'OPL-1',
}

