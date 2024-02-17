# -*- coding: utf-8 -*-
from collections import OrderedDict
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.osv.expression import OR

class CustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        stock_picking = request.env['stock.picking']
        values['picking_count'] = stock_picking.sudo().search_count([
            ('owner_id', '=', partner.id),
            ('picking_type_code','=','incoming'),
            ('is_consignment','!=',False)
        ])

        product_obj = request.env['product.product']
        line_ids = request.env['purchase.order.line'].search([
            ('partner_id', '=', partner.id),
            ('is_consignment', '=', True),
            ('state', 'in', ['purchase', 'done'])
        ])
        if line_ids:
            values['consignment_products'] = len(list(line_ids.mapped('product_id')))
        else:
            values['consignment_products'] = 0
        return values

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        stock_picking = request.env['stock.picking']
        picking_count = stock_picking.sudo().search_count([
            ('owner_id', '=', partner.id),
            ('picking_type_code','=','incoming'),
            ('is_consignment','!=',False)
        ])
        product_obj = request.env['product.product']
        # consignment_products = product_obj.sudo().search_count([
        #     ('purchase_order_line_id.partner_id', '=', partner.id),
        #     ('purchase_order_line_id', '!=', False)
        # ])
        line_ids = request.env['purchase.order.line'].search([
            ('partner_id', '=', partner.id),
            ('is_consignment', '=', True),
            ('state', 'in', ['purchase', 'done'])
        ])
        if line_ids:
            consignment_products = len(list(line_ids.mapped('product_id')))
        else:
            consignment_products = 0
        values.update({
            'picking_count': picking_count,
            'consignment_products':consignment_products,
        })
        return values

    def _consignment_picking_get_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ('product_id', 'all'):
            search_domain.append([('product_id', 'ilike', search)])
        if search_in in ('name', 'all'):
            search_domain.append([('name', 'ilike', search)])
        if search_in in ('partner_id', 'all'):
            search_domain.append([('partner_id', 'ilike', search)])
        return OR(search_domain)

    @http.route(['/my/consignment_pickings', '/my/consignment_pickings/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_consignment_pickings(self, page=1, filterby=None, sortby=None, search=None, search_in='all', **kw):
#         response = super(CustomerPortal, self)
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        picking_obj = http.request.env['stock.picking']
        domain = [
            ('owner_id', '=', partner.id),
            ('picking_type_code','=','incoming'),
            ('is_consignment','!=',False)
        ]
        # count for pager
        picking_count = picking_obj.sudo().search_count(domain)

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']
        
        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All'), 'order': 1},
            'name': {'input': 'name', 'label': ('Search in Number')},
            'product_id': {'input': 'product_id', 'label': _('Search in Product')},
            'partner_id': {'input': 'partner_id', 'label': _('Search in Vendor')},
        }
        
        if search and search_in:
            domain += self._consignment_picking_get_search_domain(search_in, search)

        # pager
        pager = portal_pager(
            url="/my/consignment_pickings",
            url_args={'sortby': sortby,'filterby': filterby},
            total=picking_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        pickings = picking_obj.sudo().search(domain, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'pickings': pickings,
            'page_name': 'consignment_picking',
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'filterby': filterby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'pager': pager,
            'default_url': '/my/consignment_pickings',
        })
        return request.render("odoo_consignment_process.display_stock_pickings_consignment", values)
    
    @http.route(['/my/consignment_product_list', '/my/consignment_product_list/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_consigment_products(self, page=1, filterby=None, sortby=None, search=None, search_in='all', **kw):
#         response = super(CustomerPortal, self)
        values = self._prepare_portal_layout_values()
        product_obj = http.request.env['product.product']
        partner = request.env.user.partner_id
        line_ids = request.env['purchase.order.line'].search([
            ('partner_id', '=', partner.id),
            ('is_consignment', '=', True),
            ('state', 'in', ['purchase', 'done'])
        ])
        if line_ids:
            product_ids = line_ids.mapped('product_id')
            domain = [('id', 'in', product_ids.ids)]
        else:
            domain = []
        # domain = [
        #     ('purchase_order_line_id.partner_id', '=', partner.id),
        #     ('purchase_order_line_id', '!=', False)
        # ]
        
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }

        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All')},
            'name': {'input': 'name', 'label': _('Search in Name')},
            'default_code': {'input': 'default_code', 'label': _('Search in Internal Reference')},
            'order_id': {'input': 'order_id', 'label': _('Search in Purchase Order')},
        }
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('default_code', 'all'):
                search_domain = OR([search_domain, [('default_code','ilike',search)]])
            if search_in in ('order_id', 'all'):
                search_domain = OR([search_domain, [('purchase_order_line_id.order_id','ilike',search)]])
            domain += search_domain

        # count for pager
        if domain:
            consignment_product_count = product_obj.sudo().search_count(domain)
        else:
            consignment_product_count = 0
        # pager
        pager = portal_pager(
            url="/my/consignment_product_list",
            url_args={'sortby': sortby,'filterby': filterby},
            total=consignment_product_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        if domain:
            consignment_products = product_obj.sudo().search(domain, limit=self._items_per_page, offset=pager['offset'])
        else:
            consignment_products = product_obj.sudo()
        values.update({
            'consignment_products': consignment_products,
            'page_name': 'consignment_product_page',
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'filterby': filterby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'pager': pager,
            'default_url': '/my/consignment_product_list',
        })
        return request.render("odoo_consignment_process.display_consignment_product_consignment", values)

    @http.route(['/my/consignment_pickings/<model("stock.picking"):picking>'], type='http', auth="user", website=True)
    def my_consignment_picking(self, picking=None, access_token=None, **kw):
        return request.render("odoo_consignment_process.display_my_consignment_detail_consignment", {'picking': picking, 'token': access_token,})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
