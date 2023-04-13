# -*- coding: utf-8 -*-
# from odoo import http


# class RailAutomaticPricelist(http.Controller):
#     @http.route('/rail_automatic_pricelist/rail_automatic_pricelist', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rail_automatic_pricelist/rail_automatic_pricelist/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rail_automatic_pricelist.listing', {
#             'root': '/rail_automatic_pricelist/rail_automatic_pricelist',
#             'objects': http.request.env['rail_automatic_pricelist.rail_automatic_pricelist'].search([]),
#         })

#     @http.route('/rail_automatic_pricelist/rail_automatic_pricelist/objects/<model("rail_automatic_pricelist.rail_automatic_pricelist"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rail_automatic_pricelist.object', {
#             'object': obj
#         })
