# -*- coding: utf-8 -*-
from odoo import http

# class MethodImportLineSo(http.Controller):
#     @http.route('/method_import_line_so/method_import_line_so/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_import_line_so/method_import_line_so/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_import_line_so.listing', {
#             'root': '/method_import_line_so/method_import_line_so',
#             'objects': http.request.env['method_import_line_so.method_import_line_so'].search([]),
#         })

#     @http.route('/method_import_line_so/method_import_line_so/objects/<model("method_import_line_so.method_import_line_so"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_import_line_so.object', {
#             'object': obj
#         })