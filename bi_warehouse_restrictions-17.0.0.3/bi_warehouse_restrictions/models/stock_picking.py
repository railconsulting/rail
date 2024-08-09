# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models,_
from odoo.osv import expression


class InheritStockPicking(models.Model):
    _inherit ="stock.picking"

    def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
        allowed_access = self.env.user.has_group('bi_warehouse_restrictions.group_restrict_operations')
        current_uid = self._context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        domains =[]
        
        if user.restrict_operation and user.restrict_location and user.restrict_warehouse_list and allowed_access:
            domain += ['|','|',
            ('picking_type_id','in',self.env.user.operation_ids.ids),
            ('location_id','in',self.env.user.location_ids.ids),
            ('picking_type_id.warehouse_id','in',self.env.user.warehouse_ids.ids),]

        elif  user.restrict_operation and user.restrict_location and allowed_access :
            domain += ['|',('picking_type_id','in',self.env.user.operation_ids.ids),('location_id','in',self.env.user.location_ids.ids)]
        elif  user.restrict_operation and user.restrict_warehouse_list and allowed_access :
            domain += ['|',('picking_type_id','in',self.env.user.operation_ids.ids),('picking_type_id.warehouse_id','in',self.env.user.warehouse_ids.ids)]
    

        elif  user.restrict_location and user.restrict_warehouse_list and allowed_access :
            domain += ['|',('location_id','in',self.env.user.location_ids.ids),('picking_type_id.warehouse_id','in',self.env.user.warehouse_ids.ids)] 

        if user.restrict_operation and allowed_access:
           domain += [('picking_type_id','in',self.env.user.operation_ids.ids)]
        elif user.restrict_location and allowed_access:
            domain += [('location_id','in',self.env.user.location_ids.ids)]
        elif user.restrict_warehouse_list and allowed_access:
            domain += [('picking_type_id.warehouse_id','in',self.env.user.warehouse_ids.ids)]

        return super(InheritStockPicking, self).search_fetch(domain, field_names, offset=0, limit=limit, order=None)

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        context = dict(self.env.context)
        allowed_access = self.env.user.has_group('bi_warehouse_restrictions.group_restrict_operations')
        current_uid = self._context.get('uid')
        user = self.env['res.users'].browse(current_uid)


        if user.restrict_operation and user.restrict_location and user.restrict_warehouse_list and allowed_access:
            domain += ['|','|',
            ('picking_type_id','in',self.env.user.operation_ids.ids),
            ('location_id','in',self.env.user.location_ids.ids),
            ('picking_type_id.warehouse_id','in',self.env.user.warehouse_ids.ids),]

        elif  user.restrict_operation and user.restrict_location and allowed_access :
            domain += ['|',('picking_type_id','in',self.env.user.operation_ids.ids),('location_id','in',self.env.user.location_ids.ids)]
        elif  user.restrict_operation and user.restrict_warehouse_list and allowed_access :
            domain += ['|',('picking_type_id','in',self.env.user.operation_ids.ids),('picking_type_id.warehouse_id','in',self.env.user.warehouse_ids.ids)]

        elif  user.restrict_location and user.restrict_warehouse_list and allowed_access :
            domain += ['|',('location_id','in',self.env.user.location_ids.ids),('picking_type_id.warehouse_id','in',self.env.user.warehouse_ids.ids)] 


        elif user.restrict_operation and allowed_access:
           domain += [('picking_type_id','in',self.env.user.operation_ids.ids)]
        elif user.restrict_location and allowed_access:
            domain += [('location_id','in',self.env.user.location_ids.ids)]
        elif user.restrict_warehouse_list and allowed_access:
            domain += [('picking_type_id.warehouse_id','in',self.env.user.warehouse_ids.ids)]

        return super(InheritStockPicking, self.sudo().with_context(context))._name_search(name, domain, operator, limit, order)
    
    

class InheritStockLocation(models.Model):
    _inherit="stock.location"
    
    @api.model
    def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
        domain = domain or []
        allowed_access = self.env.user.has_group('bi_warehouse_restrictions.group_restrict_operations')
        current_uid = self._context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        final_location_ids = user.location_ids
    
        if user.restrict_location and allowed_access:
            domain += [('id','in',final_location_ids.ids)]
            
        return super(InheritStockLocation, self).search_fetch(domain, field_names, offset=0, limit=limit, order=None)

class InheritStockWarehouse(models.Model):
    _inherit="stock.warehouse"

    @api.model
    def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
        domain = domain or []
        allowed_access = self.env.user.has_group('bi_warehouse_restrictions.group_restrict_operations')
        current_uid = self._context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        final_warehouse_ids = user.warehouse_ids
    
        if user.restrict_warehouse_list and allowed_access:
            domain += [('id','in',final_warehouse_ids.ids)]

        return super(InheritStockWarehouse, self).search_fetch(domain, field_names, offset=0, limit=limit, order=None)

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        context = dict(self.env.context)
        domain = domain or []
        allowed_access = self.env.user.has_group('bi_warehouse_restrictions.group_restrict_operations')
        current_uid = self._context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        final_warehouse_ids = user.warehouse_ids
    
        if user.restrict_warehouse_list and allowed_access:
            domain += [('id','in',final_warehouse_ids.ids)]

        return super(InheritStockWarehouse, self.sudo().with_context(context))._name_search(name, domain, operator, limit, order)
