# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_qty = fields.Float("Total Cnt.", compute="_get_total_qty", store=True)

    @api.depends('order_line','order_line.product_uom_qty')
    def _get_total_qty(self):
        for r in self:
            total = 0
            for l in r.order_line:
                total += l.product_uom_qty
            actual_pricelist = r.pricelist_id
            pricelist_obj = self.env['product.pricelist'].search([])
            new_pricelist = pricelist_obj.filtered(lambda x: total >= x.min_quantity and total <= x.max_quantity).sorted(key=lambda s:s.sequence)[:1]
            #_logger.critical("Cantidad:"+str(total))
            #_logger.critical(actual_pricelist.name)
            #_logger.critical(new_pricelist.name)
            if new_pricelist:
                r.update({
                    'total_qty': total,
                    'pricelist_id': new_pricelist.id
                })
                r._recompute_prices()
                """ r.message_post(body=_(
                    "Product prices have been recomputed according to pricelist %s.",
                    r.pricelist_id._get_html_link(),
                )) """
            else:
                r.update({
                    'total_qty': total,
                    'pricelist_id': self.env.ref('product.list0').id
                })
                r._recompute_prices()
            

