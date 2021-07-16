# -*- coding: utf-8 -*-

import base64
import datetime
import logging
import os

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

import xlrd

from flectra import models, fields, api
from datetime import timedelta

_logger = logging.getLogger(__name__)


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    id_absen = fields.Char('ID Mesin Absensi')


class hr_attendance(models.Model):
    _inherit = 'hr.attendance'

    absen_importer_id = fields.Many2one('hr.ykp.absen.importer')
    note = fields.Char('Keterangan')


class ykp_absen_importer(models.Model):
    _name = 'hr.ykp.absen.importer'
    _rec_name = 'filename'

    name = fields.Binary('Import File Xls')
    filename = fields.Char('Nama File')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('process', 'Processed')
    ], default='draft', string='State')

    @api.multi
    def action_process(self):
        self.write({'state': 'process'})
        self.process_file()

    @api.multi
    def unlink(self):
        self.env['hr.attendance'].sudo().search([('absen_importer_id', '=', self.id)]).unlink()
        return super(ykp_absen_importer, self).unlink()

    def cron_absen(self):
        employees = self.env['hr.employee'].sudo().search([])
        checkin = datetime.datetime.now()
        for employee in employees:
            attendance = self.env['hr.attendance'].search(
                [('employee_id', '=', employee.id), ('check_in', '=', checkin.strftime('%Y/%m/%d %H:%M'))])
            if not attendance:
                self.env['hr.attendance'].create({
                    'employee_id': employee.id,
                    'check_in': checkin.strftime('%Y/%m/%d %H:%M'),
                    'check_out': checkin.strftime('%Y/%m/%d %H:%M'),
                    'absen_importer_id': self.id,
                    'note': 'alfa'
                })

    def process_file(self):
        inputx = BytesIO()
        inputx.write(base64.decodestring(self.name))
        workbook = xlrd.open_workbook(file_contents=inputx.getvalue())
        sheet_names = workbook.sheet_names()
        xl_sheet = workbook.sheet_by_name(sheet_names[0])
        for row_idx in range(1, xl_sheet.nrows):  # Iterate through rows
            id_absensi = int(xl_sheet.cell(row_idx, 0).value)
            nama_pegawai = xl_sheet.cell(row_idx, 1).value
            current_date = xl_sheet.cell(row_idx, 2).value
            start_time = xl_sheet.cell(row_idx, 6).value
            end_time = xl_sheet.cell(row_idx, 7).value
            late = xl_sheet.cell(row_idx, 10).value
            early = xl_sheet.cell(row_idx, 11).value
            note = ''
            if "{}".format(xl_sheet.cell(row_idx, 2)).startswith("xldate"):
                tuple_date = xlrd.xldate.xldate_as_tuple(current_date, workbook.datemode)
                _logger.info("format :  {}".format(tuple_date))
                current_date = "{}/{}/{}".format(tuple_date[2] if tuple_date[2] > 9 else "0{}".format(tuple_date[2]),
                                                 tuple_date[1] if tuple_date[1] > 9 else "0{}".format(tuple_date[1]),
                                                 tuple_date[0])
            if late:
                if "{}".format(xl_sheet.cell(row_idx, 10)).startswith("xldate"):
                    tuple_date = xlrd.xldate.xldate_as_tuple(late, workbook.datemode)
                    late_hour = tuple_date[3]
                    late_minute = tuple_date[4]
                else:
                    late_hour = int(late.split(":")[0])
                    late_minute = int(late.split(":")[1])
                late = ((late_hour * 60) + late_minute) / 60
            else:
                late = 0.0
            if id_absensi and current_date:
                if start_time and start_time != '':
                    if "{}".format(xl_sheet.cell(row_idx, 6)).startswith("xldate"):
                        tuple_date = xlrd.xldate.xldate_as_tuple(start_time, workbook.datemode)
                        start_time = "{}:{}".format(tuple_date[3] if tuple_date[3] > 9 else "0{}".format(tuple_date[3]),
                                                    tuple_date[4] if tuple_date[4] > 9 else "0{}".format(tuple_date[4]))
                    _logger.info("start_time : {}".format(start_time))
                    checkin = datetime.datetime.strptime("{} {}".format(current_date, start_time),
                                                         '%d/%m/%Y %H:%M')
                    checkin = checkin - timedelta(hours=7)
                else:
                    checkin = False
                if end_time and end_time != '':
                    if "{}".format(xl_sheet.cell(row_idx, 7)).startswith("xldate"):
                        tuple_date = xlrd.xldate.xldate_as_tuple(end_time, workbook.datemode)
                        end_time = "{}:{}".format(tuple_date[3] if tuple_date[3] > 9 else "0{}".format(tuple_date[3]),
                                                  tuple_date[4] if tuple_date[4] > 9 else "0{}".format(tuple_date[4]))
                    checkout = datetime.datetime.strptime("{} {}".format(current_date, end_time),
                                                          '%d/%m/%Y %H:%M')
                    checkout = checkout - timedelta(hours=7)
                else:
                    if early:
                        if "{}".format(xl_sheet.cell(row_idx, 11)).startswith("xldate"):
                            tuple_date = xlrd.xldate.xldate_as_tuple(early, workbook.datemode)
                            early = "{}:{}".format(
                                tuple_date[3] if tuple_date[3] > 9 else "0{}".format(tuple_date[3]),
                                tuple_date[4] if tuple_date[4] > 9 else "0{}".format(tuple_date[4]))
                        if early == '01:00':
                            checkout = datetime.datetime.strptime("{} {}".format(current_date, '16:30'),
                                                                  '%d/%m/%Y %H:%M')
                            checkout = checkout - timedelta(hours=7)
                            note = 'checkout by system'
                        else:
                            checkout = False
                    else:
                        checkout = False

                _logger.info('id absensi : {}'.format(id_absensi))
                _logger.info("nama pegawai : {}".format(nama_pegawai))

                employee = self.env['hr.employee'].sudo().search([('id_absen', '=', id_absensi)], limit=1)
                _logger.info('id employee : {}'.format(employee.id))
                _logger.info('name employee : {}'.format(employee.name))
                if employee:
                    attendance = self.env['hr.attendance'].search(
                        [('check_in', '=', checkin.strftime('%Y/%m/%d %H:%M')), ('employee_id', '=', employee.id)],
                        limit=1)
                    if attendance:
                        attendance.write({
                            'check_in': checkin.strftime('%Y/%m/%d %H:%M') if checkin else checkin,
                            'check_out': checkout.strftime('%Y/%m/%d %H:%M') if checkout else checkout,
                            'absen_importer_id': self.id,
                            'terlambat': late,
                            'note': note
                        })
                    else:
                        self.env['hr.attendance'].create({
                            'employee_id': employee.id,
                            'check_in': checkin.strftime('%Y/%m/%d %H:%M') if checkin else checkin,
                            'check_out': checkout.strftime('%Y/%m/%d %H:%M') if checkout else checkout,
                            'absen_importer_id': self.id,
                            'terlambat': late,
                            'note': note
                        })

    def importAbsen(self):
        value = self.env['ir.config_parameter'].sudo().get_param("hr_ykp_absen.excel_path")
        if value:
            if not os.path.exists("{}/processed".format(value)):
                os.makedirs("{}/processed".format(value))
            for file in os.listdir(value):
                if file.endswith("xlsx") or file.endswith("xls"):
                    workbook = xlrd.open_workbook("{}/{}".format(value, file))
                    sheet_names = workbook.sheet_names()
                    xl_sheet = workbook.sheet_by_name(sheet_names[0])
                    # num_cols = xl_sheet.ncols  # Number of columns
                    for row_idx in range(1, xl_sheet.nrows):  # Iterate through rows
                        id_absensi = xl_sheet.cell(row_idx, 0).value
                        current_date = xl_sheet.cell(row_idx, 2).value
                        start_time = xl_sheet.cell(row_idx, 6).value
                        end_time = xl_sheet.cell(row_idx, 7).value
                        if start_time and start_time != '':
                            checkin = datetime.datetime.strptime("{} {}".format(current_date, start_time),
                                                                 '%d/%m/%Y %H:%M')
                            checkin = checkin - timedelta(hours=7)
                        else:
                            checkin = False
                        if end_time and end_time != '':
                            checkout = datetime.datetime.strptime("{} {}".format(current_date, end_time),
                                                                  '%d/%m/%Y %H:%M')
                            checkout = checkout - timedelta(hours=7)
                        else:
                            checkout = False
                        employee = self.env['hr.employee'].sudo().search([('id_absen', '=', id_absensi)], limit=1)
                        if employee:
                            attendance = self.env['hr.attendance'].search(
                                [('check_in', '=', checkin.strftime('%Y/%m/%d %H:%M')),
                                 ('employee_id', '=', employee.id)], limit=1)
                            if attendance:
                                attendance.write({
                                    'check_in': checkin.strftime('%Y/%m/%d %H:%M'),
                                    'check_out': checkout.strftime('%Y/%m/%d %H:%M')
                                })
                            else:
                                self.env['hr.attendance'].create({
                                    'employee_id': employee.id,
                                    'check_in': checkin.strftime('%Y/%m/%d %H:%M'),
                                    'check_out': checkout.strftime('%Y/%m/%d %H:%M')
                                })
                    processed_file = "{}/processed/{}".format(value, file)
                    os.rename("{}/{}".format(value, file), processed_file)
