# -*- coding: utf-8 -*-
from odoo import http

# class VctSampleModule(http.Controller):
#     @http.route('/vct_sample_module/vct_sample_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vct_sample_module/vct_sample_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vct_sample_module.listing', {
#             'root': '/vct_sample_module/vct_sample_module',
#             'objects': http.request.env['vct_sample_module.vct_sample_module'].search([]),
#         })

#     @http.route('/vct_sample_module/vct_sample_module/objects/<model("vct_sample_module.vct_sample_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vct_sample_module.object', {
#             'object': obj
#         })