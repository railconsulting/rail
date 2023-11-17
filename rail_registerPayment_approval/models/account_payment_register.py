# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class AccountPaymentRegister(models.Model):
    _inherit = 'account.payment.register'

    currency_rate_amount = fields.Float(
        string="Currency exchange rate", compute="_compute_currency_rate_amount", digits=0,
    )

    @api.depends(
        "company_id"
    )
    def _compute_currency_rate_amount(self):
        for item in self:
            item.currency_rate_amount = 1