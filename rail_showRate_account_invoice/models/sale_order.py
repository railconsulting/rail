# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    currency_rate_amount = fields.Float(
        string="Tipo de cambio", compute="_compute_currency_rate_amount", digits=0,
    )