# -*- coding: utf-8 -*-
# from odoo import http


# class TodooKronos(http.Controller):
#     @http.route('/suprapak_kronos/suprapak_kronos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/suprapak_kronos/suprapak_kronos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('suprapak_kronos.listing', {
#             'root': '/suprapak_kronos/suprapak_kronos',
#             'objects': http.request.env['suprapak_kronos.suprapak_kronos'].search([]),
#         })

#     @http.route('/suprapak_kronos/suprapak_kronos/objects/<model("suprapak_kronos.suprapak_kronos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('suprapak_kronos.object', {
#             'object': obj
#         })
