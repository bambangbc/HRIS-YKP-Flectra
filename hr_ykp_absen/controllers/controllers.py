# -*- coding: utf-8 -*-
from flectra import http

# class YkpAbsen(http.Controller):
#     @http.route('/ykp_absen/ykp_absen/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ykp_absen/ykp_absen/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ykp_absen.listing', {
#             'root': '/ykp_absen/ykp_absen',
#             'objects': http.request.env['ykp_absen.ykp_absen'].search([]),
#         })

#     @http.route('/ykp_absen/ykp_absen/objects/<model("ykp_absen.ykp_absen"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ykp_absen.object', {
#             'object': obj
#         })