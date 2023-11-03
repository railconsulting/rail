# -*- coding: utf-8 -*-

from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_currency_rate = fields.Floats(string="Tipo de cambio")