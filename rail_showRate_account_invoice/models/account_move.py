# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    currency_rate_amount = fields.Float(
        string="Tipo de cambio", compute="_compute_currency_rate_amount", digits=0,
    )

    def _get_rates(self, company, date):
        if not self.ids:
            return {}
        self.env['res.currency.rate'].flush_model(['rate', 'currency_id', 'company_id', 'name'])
        query = """SELECT c.id,
                          COALESCE((SELECT r.rate FROM res_currency_rate r
                                  WHERE r.currency_id = c.id AND r.name = %s
                                    AND (r.company_id IS NULL OR r.company_id = %s)
                               ORDER BY r.company_id, r.name DESC
                                  LIMIT 1), 1.0) AS rate
                   FROM res_currency c
                   WHERE c.id IN %s"""
        self._cr.execute(query, (date, company.id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        return currency_rates

    @api.depends(
        "state",
        "date",
        "line_ids.amount_currency",
        "company_id",
        "currency_id"
    )
    def _compute_currency_rate_amount(self):
        for item in self:
            #rates = item.currency_id._get_rates(item.company_id, item.date)
            rates = self._get_rates(item.company_id, item.date)
            if item.currency_id != item.company_id.currency_id:
                if rates.get(item.currency_id.id) is not None:
                    item.currency_rate_amount = 1/rates.get(item.currency_id.id)
                else:
                    item.currency_rate_amount = -1
                    raise ValidationError('Currency Rate not found' + str(item.date))
            else:
                item.currency_rate_amount = 1
