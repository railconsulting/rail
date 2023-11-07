# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    currency_rate_amount = fields.Float(
        string="Tipo de cambio", compute="_compute_currency_rate_amount", digits=0,
    )

    @api.depends(
        "date_order",
        "company_id",
        "currency_id"
    )
    def _compute_currency_rate_amount(self):
        currencyRate=0
        
        for item in self:
            if item.currency_id != item.company_id.currency_id:
                rates = self.get_rates(item.currency_id, item.company_id, item.date_order)
                currencyRate = rates.get(item.currency_id.id)
                if currencyRate == 1.0:
                    item.currency_rate_amount = -1
                    raise ValidationError('Currency rate not found for date ' + str(item.date_order))
                else:
                    item.currency_rate_amount = 1/currencyRate
            else:
                item.currency_rate_amount = 1