# -*- coding: utf-8 -*-
from flectra import http

# class HrYkpRecruitment(http.Controller):
#     @http.route('/hr_ykp_recruitment/hr_ykp_recruitment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_ykp_recruitment/hr_ykp_recruitment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_ykp_recruitment.listing', {
#             'root': '/hr_ykp_recruitment/hr_ykp_recruitment',
#             'objects': http.request.env['hr_ykp_recruitment.hr_ykp_recruitment'].search([]),
#         })

#     @http.route('/hr_ykp_recruitment/hr_ykp_recruitment/objects/<model("hr_ykp_recruitment.hr_ykp_recruitment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_ykp_recruitment.object', {
#             'object': obj
#         })