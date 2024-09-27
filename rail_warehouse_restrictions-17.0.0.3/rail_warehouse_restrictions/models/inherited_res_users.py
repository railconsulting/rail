# -*- coding: utf-8 -*-
# Property of Rail Consulting.  See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models


class InheritResUsers(models.Model):
    _inherit = 'res.users'


    restrict_operation = fields.Boolean(string="Restringir Operación")
    restrict_location = fields.Boolean(string="Restringir Ubicación")
    restrict_warehouse_list = fields.Boolean(string="Restringir Almacén")

    warehouse_ids = fields.Many2many('stock.warehouse','rel_warehouse_restrictions', string="Almacén Permitido")
    location_ids = fields.Many2many('stock.location', string="Ubicación Permitida",check_company=True)
    operation_ids = fields.Many2many('stock.picking.type', string="Operaciones de Almaceén Permitidas")


    @api.onchange('restrict_operation')
    def _onchange_restrict_operation(self):
        if self.restrict_operation == False:
            self.operation_ids=[(6,0,[])]
        

    @api.onchange('restrict_location')
    def _onchange_restrict_location(self):
        if self.restrict_location == False :
            self.location_ids=[(6,0,[])]

    @api.onchange('restrict_warehouse_list')
    def _onchange_restrict_warehouse_list(self):
        if self.restrict_warehouse_list == False:
            self.warehouse_ids=[(6,0,[])]
    

    



