# -*- coding: utf-8 -*-

from odoo import fields, models, api

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    discount_amount = fields.Float('Discount Amount', digits='Product Price')
    amount_due = fields.Float(compute='_compute_amount_due', digits='Product Price', store=True)

    @api.depends('amount_total', 'discount_amount')
    def _compute_amount_due(self):
        for record in self:
            record.amount_due = record.amount_total - record.discount_amount