# -*- coding: utf-8 -*-
{
	'name': "Rail Automatic Pricelist",

	'summary': """
        Create rules to apply pricelist based on product quantity""",

	'author': "RAIL / Kevin Lopez",
	'website': "https://www.rail.com.mx",

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
	# for the full list
	'category': 'Sales',
	'version': '0.1',

	# any module necessary for this one to work correctly
	'depends': ['point_of_sale', 'sale_management'],

	# always loaded
	'data': [
		# 'security/ir.model.access.csv',
		'views/pricelist.xml',
		'views/sale_order.xml',
	],
	'assets': {
		'point_of_sale.assets': [
			'rail_automatic_pricelist/static/src/js/models/models.js',
			'rail_automatic_pricelist/static/src/js/ProductScreen/ProductScreen.js',
			'rail_automatic_pricelist/static/src/js/models/order_summary.js',
			'rail_automatic_pricelist/static/src/xml/OrderSummary.xml',
		]
	},
	# only loaded in demonstration mode
	'demo': [
		'demo/demo.xml',
	],
}
