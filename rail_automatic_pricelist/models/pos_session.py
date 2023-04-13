from datetime import datetime

from odoo import models, api, fields, _


class PosSession(models.Model):
	_inherit = 'pos.session'

	def _loader_params_product_pricelist(self):
		"""
		Min Quantity & Max Quantity in param's fields
		:return: params
		"""
		params = super(PosSession, self)._loader_params_product_pricelist()
		if 'search_params' in params:
			params.get('search_params', {}).get('fields', []).append('min_quantity')
			params.get('search_params', {}).get('fields', []).append('max_quantity')
			params.get('search_params', {}).get('fields', []).append('sequence')
		return params
