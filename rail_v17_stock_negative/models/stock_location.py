# ©  2008-2021 Rail Consulting
# See README.rst file on addons root folder for license details


from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    allow_negative_stock = fields.Boolean(string="Permitir stock en negativo")
