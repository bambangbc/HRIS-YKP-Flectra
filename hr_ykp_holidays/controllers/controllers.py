# -*- coding: utf-8 -*-
import os

from flectra import http
from flectra.http import request, content_disposition


class Controller(http.Controller):
    @http.route('/hr_ykp_holidays/download/<id>/', type='http', auth="user", website=True)
    def download_document(self, id):
        perdin = http.request.env['hr.perdin'].search([('id', '=', id)], limit=1)
        path = os.path.dirname(os.path.realpath(__file__))
        filename = "{}/../reports/report_perdin_{}.xlsx".format(path, perdin.name.replace("/", "_"))
        with open(filename, "rb") as handle:
            filecontent = handle.read()
        return request.make_response(filecontent,
                                     [('Content-Type', 'application/octet-stream'),
                                      ('Content-Disposition', content_disposition("report_perdin.xlsx"))])
