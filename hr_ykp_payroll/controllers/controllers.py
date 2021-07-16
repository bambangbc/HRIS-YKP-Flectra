# -*- coding: utf-8 -*-
import os

from flectra import http
from flectra.http import request, content_disposition


class Controller(http.Controller):

    @http.route('/payroll/download/<date>/', type='http', auth="user", website=True)
    def download_payroll(self, date):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = "{}/../reports/report_payslip_{}_{}.xlsx".format(path, date[4:len(date)], date[0:4])
        with open(filename, "rb") as handle:
            filecontent = handle.read()
        return request.make_response(filecontent,
                                     [('Content-Type', 'application/octet-stream'),
                                      ('Content-Disposition', content_disposition("report_payslip.xlsx"))])

    @http.route('/hr_pajak/download/<month>/<year>/', type='http', auth="user", website=True)
    def download_document(self, month, year):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = "{}/../reports/report_pajak_periode_{}_{}.xlsx".format(path, month, year)
        with open(filename, "rb") as handle:
            filecontent = handle.read()
        return request.make_response(filecontent,
                                     [('Content-Type', 'application/octet-stream'),
                                      ('Content-Disposition', content_disposition("report_pajak.xlsx"))])
