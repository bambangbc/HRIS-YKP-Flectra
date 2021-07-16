# -*- coding: utf-8 -*-
import pdfkit
import unicodedata

from flectra import http
from flectra.http import request, content_disposition


class HrYkpTraining(http.Controller):

    @http.route('/web/binary/download_document', type='http', auth="public")
    def index(self, model, id, filename=None, **kw):
        Model = request.env[model]
        res = Model.search([('id', '=', id)], limit=1)
        if res:
            escaped = u''.join(res.assignment_letter)
            escaped = unicodedata.normalize('NFKD', escaped).encode('ascii', 'ignore')
            options = {
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in'
            }
            escaped = escaped.decode('utf-8')
            print(type(escaped))
            pdf = pdfkit.from_string(escaped, False, options=options)
            if not filename or not filename.endswith('pdf'):
                filename = "surat_tugas.pdf"
            return request.make_response(pdf,
                                         [('Content-Type', 'application/octet-stream'),
                                          ('Content-Disposition', content_disposition(filename))])
        else:
            return 'not found'