# ©  2008-2021 Rail Consulting
# See README.rst file on addons root folder for license details


from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    no_negative_stock = fields.Boolean(
        string="No permitir stock en negativo",
        help="Evita el registro de transacciones con existencias en negativo.",
    )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    no_negative_stock = fields.Boolean(
        related="company_id.no_negative_stock",
        string="No permitir stock en negativo",
        readonly=False,
        help="Evita el registro de transacciones con existencias en negativo.",
    )
