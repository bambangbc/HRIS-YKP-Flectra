# -*- coding: utf-8 -*-
from flectra import http

# class HrYkpAppraisal(http.Controller):
#     @http.route('/hr_ykp_appraisal/hr_ykp_appraisal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_ykp_appraisal/hr_ykp_appraisal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_ykp_appraisal.listing', {
#             'root': '/hr_ykp_appraisal/hr_ykp_appraisal',
#             'objects': http.request.env['hr_ykp_appraisal.hr_ykp_appraisal'].search([]),
#         })

#     @http.route('/hr_ykp_appraisal/hr_ykp_appraisal/objects/<model("hr_ykp_appraisal.hr_ykp_appraisal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_ykp_appraisal.object', {
#             'object': obj
#         })