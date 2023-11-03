# -*- coding: utf-8 -*-

from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    x_studio_tc = fields.Floats(string="Tipo de cambio")