# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SalePricelist(models.Model):
    _inherit = 'product.pricelist'

    min_quantity = fields.Float("Cantidad minima")
    max_quantity = fields.Float("Cantidad maxima")

    @api.onchange('min_quantity')
    def _onchange_min_quantity(self):
        for r in self:
            r.update({
                'max_quantity': r.min_quantity
            })
    
    @api.onchange('max_quantity')
    def _onchange_max_quantity(self):
        for r in self:
            if r.min_quantity > 0 and  r.max_quantity < r.min_quantity:
                raise ValidationError("La cantidad minima no puede ser mayor a la cantidad maxima")
