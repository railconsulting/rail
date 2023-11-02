# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    currency_rate_amount = fields.Float(string="Currency Rate", compute="_compute_currency_rate_amount", digits=0
    )
        
    @api.depends(
            "date",
            "company_id",
            "currency_id"
    )
    def _compute_currency_rate_amount(self):
        #Initializing currency_rate_amount
        self.currency_rate_amount = 1

        for item in self:

            rates = item.currency_id._get_rates(item.company_id, item.date)
            item.currency_rate_amount = rates.get(item.currency_id.id)