# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.
import base64
import logging

from flectra import api, fields, models
from flectra import tools, _
from flectra.exceptions import ValidationError, AccessError
from flectra.modules.module import get_module_resource

class Hr_employee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'




    nik                     = fields.Char(string="NIP")
    npwp                    = fields.Char(string="NPWP")
    no_kk                   = fields.Char(string='No.KK')
    Place_of_bird           = fields.Char(string="Place Of Bird")
    relgion                 = fields.Many2one('hr.religion',string="Religion")
    jumlah_tanggungan       = fields.Float(string="Jumlah Tanggungan")
    alamat_ktp              = fields.Char(string="KTP Address")
    state_id                = fields.Many2one(comodel_name="hr.state", string="state")
    city_id                 = fields.Many2one(comodel_name="hr.city", string="City")
    kecamatan_id            = fields.Many2one(comodel_name="hr.kecamatan", string="Kecamatan")
    kelurahan_id            = fields.Many2one(comodel_name="hr.kelurahan", string="Kelurahan")
    rt_rw                   = fields.Char(string="RT/RW")
    zip_code                = fields.Char(string="Zip Code")

    alamat2                 = fields.Char(string="Address")
    state_id2               = fields.Many2one(comodel_name="hr.state2", string="state")
    city_id2                = fields.Many2one(comodel_name="hr.city2", string="City")
    kecamatan_id2           = fields.Many2one(comodel_name="hr.kecamatan2", string="Kecamatan")
    kelurahan_id2           = fields.Many2one(comodel_name="hr.kelurahan2", string="Kelurahan")
    rt_rw2                  = fields.Char(string="RT/RW")

    gol_darah               = fields.Char(string="Blood Type")
    warna_kulit             = fields.Char(string="Skin C0lor")
    bentuk_wajah            = fields.Char(string="Face Shape")
    jenis_rambut            = fields.Char(string="Hair Type")
    tinggi_bb               = fields.Char(string="height and weight")

    name_darurat            = fields.Char(string="Name")
    hubungan_darurat        = fields.Char(string="status")
    handphone_darurat       = fields.Char(string="handphone")
    alamat_darurat          = fields.Char(string="Address")
    state_id_darurat               = fields.Many2one(comodel_name="hr.state.darurat", string="state")
    city_id_darurat                = fields.Many2one(comodel_name="hr.city.darurat", string="City")
    kecamatan_id_darurat           = fields.Many2one(comodel_name="hr.kecamatan.darurat", string="Kecamatan")
    kelurahan_id_darurat           = fields.Many2one(comodel_name="hr.kelurahan.darurat", string="Kelurahan")
    rt_rw_darurat                  = fields.Char(string="RT/RW")
    zip_code_darurat               = fields.Char(string="Zip Code")

    no_bpjs                        = fields.Char(string="Nomor BPJS")
    faskes                         = fields.Char(string="Faskes Tingkat")
    dokter_gigi                    = fields.Char(string="Dokter Gigi")

    unit_kerja                     = fields.Char(string="Unit Kerja")
    penempatan                     = fields.Char(String="Placement")
    jenis_pegawai                  = fields.Char(string="Type Of Employee")
    jabatan                        = fields.Char(string="Position")
    masa_jabatan                   = fields.Char(string="Masa Jabatan")
    grade                          = fields.Char(string="Grade")
    masa_grade                     = fields.Char(string="Masa Grade")
    tanggal_masuk                  = fields.Char(string="Date in")
    masa_kerja                     = fields.Char(string="Masa Kerja")
    tanggal_pengangkatan           = fields.Char(string="Tanggal Pengangkatan")
    tanggal_pensiun                = fields.Char(string="Pension Date")
    tanggal_keluar                 = fields.Char(string="Date Out")
    tahun_cuti_besar               = fields.Char(string="Year Of Big Leave")
    no_jamsostek                   = fields.Char(string="Jamsostek Number")
    no_npwp                        = fields.Char(string="NPWP Number")
    potongan_asuransi_jiwa         = fields.Char(string="Pieces Of Life Insurance")
    status_nikah_pajak_TB          = fields.Char(string="Status Nikah Pajak (TB)")
    status_nikah_pajak_TD          = fields.Char(string="Status Nikah Pajak (TD)")
    jum_tanggungan_TB              = fields.Char(string="Jumlah Tanggungan Tahun Berjalan")
    jum_tanggungan_TD              = fields.Char(string="Jumlah Tanggungan Tahun Depan")
    program_karir                  = fields.Char(string="Program Karir")

    family_ids = fields.One2many(comodel_name="hr.employee.family", inverse_name="employee_id", string="Family")
    education_ids = fields.One2many(comodel_name="hr.education", string="Education Formal", inverse_name="employee_id")
    organization_ids = fields.One2many(comodel_name="hr.organization", string="Organization History", inverse_name="employee_id")
    certification_ids = fields.One2many(comodel_name="hr.certification", string="Certification", inverse_name="employee_id")




class Hr_religion(models.Model):
    _name = 'hr.religion'

    name                    = fields.Char(string="Name")

class Hr_state(models.Model):
    _name = 'hr.state'

    name                    = fields.Char(string="Name")

class Hr_city(models.Model):
    _name = 'hr.city'

    name                    = fields.Char(string="Name")

class Hr_kecamatan(models.Model):
    _name = 'hr.kecamatan'

    name                    = fields.Char(string="Name")

class Hr_kelurahan(models.Model):
    _name = 'hr.kelurahan'

    name                    = fields.Char(string="Name")

class Hr_state2(models.Model):
    _name = 'hr.state2'

    name                    = fields.Char(string="Name")

class Hr_city2(models.Model):
    _name = 'hr.city2'

    name                    = fields.Char(string="Name")

class Hr_kecamatan2(models.Model):
    _name = 'hr.kecamatan2'

    name                    = fields.Char(string="Name")

class Hr_kelurahan2(models.Model):
    _name = 'hr.kelurahan2'

    name                    = fields.Char(string="Name")

class Hr_state_darurat(models.Model):
    _name = 'hr.state.darurat'

    name                    = fields.Char(string="Name")

class Hr_city_darurat(models.Model):
    _name = 'hr.city.darurat'

    name                    = fields.Char(string="Name")

class Hr_kecamatan_darurat(models.Model):
    _name = 'hr.kecamatan.darurat'

    name                    = fields.Char(string="Name")

class Hr_kelurahan_darurat(models.Model):
    _name = 'hr.kelurahan.darurat'

    name                    = fields.Char(string="Name")

class Hr_employee_family(models.Model):
    _name = 'hr.employee.family'

    family  = fields.Selection([('suami_istri', 'Istri / Suami'),
                                ('saudara_kandung', 'Saudara Kandung'),
                                ('ayah', 'Ayah'),
                                ('ibu', 'Ibu'),
                                ('anak1', 'Anak ke 1'),
                                ('anak2', 'Anak ke 2'),
                                ('anak3', 'Anak ke 3'),],string='Anggota Keluarga', required=True)
    name = fields.Char(string="Name", required=True)
    jenis_kelamin = fields.Selection([('l', 'Laki-Laki'),
                                    ('p', 'Perempuan'),],  string='Jenis Kelamin', required=True)
    jenjang  = fields.Many2one(comodel_name="hr.degree", string="Pendidikan")
    age = fields.Integer(string="Usia", required=True)
    address = fields.Char(string="Alamat", required=True)
    work = fields.Char(string="Pekerjaan", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_degree(models.Model):
    _name = 'hr.degree'

    name = fields.Char(string="Name")

class Hr_employee_education_formal(models.Model):
    _name = 'hr.education'

    name  = fields.Many2one(comodel_name="hr.degree", string="Degree", required=True)
    kampus = fields.Char(string="University", required=True)
    fakultas = fields.Char(string="Faculty", required=True)
    jurusan = fields.Char(string="Department", required=True)
    end_year = fields.Char(string="Graduation year", required=True)
    ipk = fields.Char(string="IPK")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_organization(models.Model):
    _name = 'hr.organization'

    name  = fields.Char(string="Organization Name", required=True)
    start_date = fields.Char(string="start Date", required=True)
    end_date = fields.Char(string="End Date", required=True)
    position = fields.Char(string="Last Position", required=True)
    honor = fields.Char(string="Last Honorarium")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_certification(models.Model):
    _name = 'hr.certification'

    name  = fields.Char(string="Certification Name", required=True)
    lembaga = fields.Char(string="Institution", required=True)
    date = fields.Char(string="Date", required=True)
    end_date = fields.Char(string="End Date", required=True)
    no_sertifikat = fields.Char(string="Sertification Number", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")