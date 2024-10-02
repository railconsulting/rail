from odoo import models,fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    bizylife_purchase_order = fields.Binary()
