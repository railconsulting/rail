# -*- coding: utf-8 -*-
{
    'name': "Urban Purchase agreements customizations",

    'summary': """
        New purchase agreements features for Urban""",


    'author': "Rail / Kevin Lopez",
    'website': "https://www.rail.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock','purchase','purchase_requisition','report_xlsx','mail','contacts'],

    # always loaded
    'data': [
        'views/mail_view.xml',
        'security/ir.model.access.csv',
        'data/settings.xml',
        'data/purchase_security.xml',   
        'data/purchase_requisition_data.xml',
        'data/bl_email_template.xml',
        'wizard/import_blanket_line.xml',
        'views/purchase_order.xml',
        'views/pr_blanket_view.xml',
        'views/purchase_requisition_type.xml',
        'views/purchase_requisition.xml',
        'views/templates.xml',
        'views/stock_picking.xml',
        'reports/delivery_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    "license": "LGPL-3",

}
