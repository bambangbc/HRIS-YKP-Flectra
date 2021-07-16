# -*- coding: utf-8 -*-
import os

from flectra import http
from flectra.http import request, content_disposition


class Controller(http.Controller):
    @http.route('/hr_ykp_lembur/download/<date>/', type='http', auth="user", website=True)
    def download_document(self, date):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = "{}/../reports/report_lembur_{}_{}.xlsx".format(path, date[0:10], date[10:len(date)])
        with open(filename, "rb") as handle:
            filecontent = handle.read()
        return request.make_response(filecontent,
                                     [('Content-Type', 'application/octet-stream'),
                                      ('Content-Disposition', content_disposition("report_lembur.xlsx"))])
