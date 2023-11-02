# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    currency_rate_amount = fields.Float(
        string="Rate", compute="_compute_currency_rate_amount", digits=0
    )

    show_currency_rate_amount = fields.Boolean(
        compute="_compute_show_currency_rate_amount", readonly=True
    )
        
    @api.depends(
            "date",
            "company_id",
            "currency_id",
            "show_currency_rate_amount"
    )

    def _compute_currency_rate_amount(self):
        #Initializing currency_rate_amount
        self.currency_rate_amount = 1

        for item in self.filtered("show_currency_rate_amount"):

            rates = item.currency_id._get_rates(item.company_id, item.date)
            item.currency_rate_amount = rates.get(item.currency_id.id)

    @api.depends(
        "currency_id", 
        "currency_ud.rate_ids", 
        "company_id")
    
    def _compute_show_cyrrency_rate_amount(self):
        for item in self:
            item.show_currency_rate_amount = (
                item.currency_id != item.company_id.currency_id
            )