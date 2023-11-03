# -*- coding: utf-8 -*-

from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    use_jedd = fields.Boolean(string="Prueba JEDD")