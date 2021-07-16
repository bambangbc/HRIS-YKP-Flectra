# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from flectra import api, fields, models, _
from flectra.exceptions import UserError

import datetime
from datetime import datetime, timedelta
from datetime import time as datetime_time
import csv

class Hrpph21Employees(models.TransientModel):
	_name = "hr.pph21.employees"
	_description = "Generate pph21 For All Selected emplployee"

	employee_ids = fields.Many2many('hr.employee', 'hr_pph21_group_rel', 'periode_id','employee_id','Employees')

	@api.multi
	def compute_sheet(self):
		pph21 = self.env['hr.pajak']
		[data] = self.read()
		active_id = self.env.context.get('active_id')
		if active_id:
			[run_data] = self.env['hr.pajak.periode'].browse(active_id).read(['month', 'year'])
		month = run_data.get('month')
		year = run_data.get('year')
		if not data['employee_ids']:
			raise UserError(_("You must select employee(s) to generate payslip(s)."))
		for employee in self.env['hr.employee'].browse(data['employee_ids']):
			#pph21_data = pph21.onchange_employee(employee.id,month,years)
			date_to = datetime(int(year), month, 26).strftime('%Y-%m-%d')
			date_one = datetime(int(year), 1, 1).strftime('%Y-%m-%d')
			payslips = self.env['hr.payslip'].search(
				[('employee_id', '=', employee.id), ('date_to', '<=', date_to),('date_to','>=', date_one)])
			gaji = 0
			asuransi = 0
			potongan = 0
			salary = 0
			dplk = 0
			bpjstk = 0
			bpjskes = 0
			potongan_dplk = 0
			pot_bpjstk = 0
			pot_dplk_i = 0
			pot_bpjstk_i = 0
			pot_bpjskes = 0
			bpjstk_jkm = 0
			bpjstk_jkk = 0
			pot_bpjskes_i = 0
			bpjstk_jkm_i = 0
			bpjstk_jkk_i = 0
			pot_kehadiran = 0
			pot_absensi = 0
			pot_dplk = 0
			mth = 0
			mth_dari = 12	
			for payslip in payslips:
				pot_kehadiran = 0
				pot_absensi = 0
				salary = payslip.single_salary
				for detail in payslip.line_ids :
					if detail.code == "PK" :
						pot_kehadiran =detail.total
					if detail.code == "PA" :
						pot_absensi = detail.total
				
				# paktor penambah
				gaji += salary + pot_kehadiran + pot_absensi
				bpjstk_jkk_i = payslip.single_salary * (payslip.employee_id.jenis_pegawai.jkk/100)
				bpjstk_jkm_i = payslip.single_salary * (payslip.employee_id.jenis_pegawai.jkm/100)
				bpjskes_i = payslip.tunj_bpjskes

				bpjstk_jkk += payslip.single_salary * (payslip.employee_id.jenis_pegawai.jkk/100)
				bpjstk_jkm += payslip.single_salary * (payslip.employee_id.jenis_pegawai.jkm/100)
				bpjskes += payslip.tunj_bpjskes

				#paktor Pengurang
				pot_dplk_i = payslip.potongan_dplk
				pot_bpjstk_i = payslip.pot_bpjstk

				pot_dplk += payslip.potongan_dplk
				pot_bpjstk += payslip.pot_bpjstk

				months = datetime.strptime(payslip.date_to,"%Y-%m-%d").month
				if month < mth_dari :
					masa_dari = months
				if month > mth :
					masa_sampai = months 
				mth = months
				mth_dari = months
			for i in range(month, 12):

				#faktor penambah
				gaji += salary
				bpjstk_jkk += bpjstk_jkk_i
				bpjstk_jkm += bpjstk_jkm_i
				bpjskes += bpjskes_i
				
				#faktor pengurang
				pot_dplk += pot_dplk_i
				pot_bpjstk += pot_bpjstk_i
			biaya_jabatan = gaji * 0.05 
			## hitung pajak
			pajak_real = 0
			pkp_setahun = 0
			cek = True
			i = 0
			pajak_sebelum = 0
			while cek == True and i < 100 :       
				jum_bruto = gaji + bpjstk_jkk + bpjstk_jkm + bpjskes + pajak_sebelum
				biaya_jabatan = jum_bruto * 0.05
				jum_pengurang = biaya_jabatan + pot_dplk + pot_bpjstk
				jum_neto = jum_bruto - jum_pengurang
				pkp_sthn = jum_neto - employee.status_pajak.nominal_tahun 
				if pkp_sthn > 1000 : 
					pkp_setahun = int(str(int(pkp_sthn))[:len(str(int(pkp_sthn)))-3]+"000")
				pajak_real = 0
				#import pdb;pdb.set_trace()
				for pkp in self.env['hr.pkp'].search([]) :
					pajak = 0
					if pkp_setahun > pkp.nominal_max :
						total_ptkp = pkp.nominal_max - pkp.nominal_mix
						pajak = total_ptkp * pkp.pajak
					elif pkp_setahun <= pkp.nominal_max and pkp_setahun >= pkp.nominal_mix :
						pjk = pkp_setahun - pkp.nominal_mix
						pajak = pjk * pkp.pajak
					pajak_real = pajak_real + pajak
				pph21 = pajak_real
				#self.pph21 = (self.pkp_setahun - rumus_pkp.nominal_mix) * rumus_pkp.pajak
				if pph21 == pajak_sebelum :
					cek = False
				if pph21 != pajak_sebelum :
					pajak_sebelum = pph21
				i += 1
			pph21_sebulan = pph21/12
			pph21_des = 0
			if month == 12 :			
				periods = self.env['hr.pajak.periode'].search(
				[('year', '=', self.periode_id.year), ('month', '<', 12)])
				for period in periods :
					pajaks = self.env["hr.pajak"].search([("employee_id","=",employee_id.id)], limit=1)
					for pajak in pajaks :
						pph21_final += self.pph21_sebulan
				pph21_des = self.tunj_pajak - pph21_final + self.penyesuaian
			res = {
				'employee_id': employee.id,
				'periode_id': active_id,
				'status': employee.status_pajak.id,
				'masa_dari': masa_dari,
				'masa_sampai': masa_sampai,
				'gaji':gaji,
				'tunj_pajak': pph21,
				'lembur': 0,
				'perdin': 0,
				'diklat': 0,
				'bpjstk_jkk': bpjstk_jkk,
				'bpjstk_jkm': bpjstk_jkm,
				'bpjskes': bpjskes,
				'pre_asuransi': bpjstk_jkk+bpjstk_jkm+bpjskes,
				'biaya_jabatan': biaya_jabatan,
				'pot_dplk': pot_dplk,
				'pot_bpjstk': pot_bpjstk,
				'iuran': pot_dplk+pot_bpjstk,
				'jum_bruto': jum_bruto,
				'jum_pengurang': jum_pengurang,
				'jum_neto': jum_neto,
				'jum_neto_pph21': jum_neto,
				'ptkp': employee.status_pajak.nominal_tahun,
				'pkp_setahun': pkp_setahun,
				'pph21': pph21,
				'pph21_sebulan': pph21_sebulan,
				'pph21_des': pph21_des,

			}
			self.env['hr.pajak'].create(res)
		#with open('names.csv', 'w', newline='') as csvfile:
		#	fieldnames = ['first_name', 'last_name']
		#	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		#	writer.writeheader()
		#	writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
		#	writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
		#	writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

		#import pdb;pdb.set_trace()
		#pph21.compute_sheet()
		return {'type': 'ir.actions.act_window_close'}