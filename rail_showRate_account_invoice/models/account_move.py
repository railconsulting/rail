# -*- coding: utf-8 -*-

from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    currency_rate_amount = fields.Float(
        string="Tipo de cambio", compute="_compute_currency_rate_amount", digits=0,
    )

    @api.depends(
        "state",
        "date",
        "line_ids.amount_currency",
        "company_id",
        "currency_id"
    )
    def _compute_currency_rate_amount(self):
        for item in self:
            rates = item.currency_id._get_rates(item.company_id, item.date)
            item.currency_rate_amount = rates