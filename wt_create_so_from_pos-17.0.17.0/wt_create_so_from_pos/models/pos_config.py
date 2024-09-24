from odoo import _, api, fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"


    create_so = fields.Boolean("Crear Orden de Venta", help="Permite crear una Orden de Venta desde el PdV", default=True)