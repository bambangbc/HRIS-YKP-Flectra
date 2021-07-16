# -*- coding: utf-8 -*-
from flectra import http

# class Debranding(http.Controller):
#     @http.route('/debranding/debranding/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/debranding/debranding/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('debranding.listing', {
#             'root': '/debranding/debranding',
#             'objects': http.request.env['debranding.debranding'].search([]),
#         })

#     @http.route('/debranding/debranding/objects/<model("debranding.debranding"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('debranding.object', {
#             'object': obj
#         })