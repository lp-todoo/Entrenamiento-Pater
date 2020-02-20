# -*- coding: utf-8 -*-
# from odoo import http


# class Pater(http.Controller):
#     @http.route('/pater/pater/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pater/pater/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pater.listing', {
#             'root': '/pater/pater',
#             'objects': http.request.env['pater.pater'].search([]),
#         })

#     @http.route('/pater/pater/objects/<model("pater.pater"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pater.object', {
#             'object': obj
#         })
