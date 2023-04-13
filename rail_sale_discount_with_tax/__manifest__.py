# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Discount after tax calculation',
    'version': '16.0.0.1',
    'category': 'Sales',
    'summary': 'Sale discount sales discount invoice discount with tax amount global discount',
    'description': """
""",
    "license":'OPL-1',
    'author': 'Rail Consulting / Kevin Lopez',
    'website': 'https://rail.com.mx',
    'images': [],
    'depends': ['base','sale','sale_management','account','stock'],
    'data': [
        'views/sale_view.xml',
        'report/inherit_sale_report.xml',
        'report/inherit_account_report.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'live_test_url': "https://youtu.be/2IVfRyBo5LU",
    'images':['static/description/Banner.gif'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
