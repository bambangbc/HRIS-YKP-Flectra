# -*- coding: utf-8 -*-
from flectra import http

# class FlectraAdvanceSearch(http.Controller):
#     @http.route('/flectra_advance_search/flectra_advance_search/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/flectra_advance_search/flectra_advance_search/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('flectra_advance_search.listing', {
#             'root': '/flectra_advance_search/flectra_advance_search',
#             'objects': http.request.env['flectra_advance_search.flectra_advance_search'].search([]),
#         })

#     @http.route('/flectra_advance_search/flectra_advance_search/objects/<model("flectra_advance_search.flectra_advance_search"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('flectra_advance_search.object', {
#             'object': obj
#         })