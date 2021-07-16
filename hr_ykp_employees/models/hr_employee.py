# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.
import base64
import logging

from flectra import api, fields, models
from flectra import tools, _
from flectra.exceptions import ValidationError, AccessError
from flectra.modules.module import get_module_resource

class Hr_contract(models.Model):
    _name = 'hr.contract'
    _inherit = 'hr.contract'

    contract_number = fields.Char(string="Contract Number")

Hr_contract()

class res_users(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'
    
    employee_id = fields.Many2one('hr.employee',string="Employee")
    
res_users()

class Hr_employee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'

    nik                     = fields.Char(string="NIP")
    npwp                    = fields.Char(string="NPWP")
    no_kk                   = fields.Char(string='No.KK')
    place_of_birth          = fields.Char(string="Tempat Lahir")
    relgion                 = fields.Many2one('hr.religion',string="Agama")
    jumlah_tanggungan       = fields.Float(string="Jumlah Tanggungan")
    alamat_ktp              = fields.Char(string="Alamat Sesuai KTP")
    gelar                   = fields.Char(string="Gelar")
    state_id                = fields.Many2one(comodel_name="hr.state", string="Provinsi",domain="[('country_id','=',country_id)]")
    city_id                 = fields.Many2one(comodel_name="hr.city", string="Kota", domain="[('provinsi_id','=',state_id)]")
    kecamatan_id            = fields.Many2one(comodel_name="hr.kecamatan", string="Kecamatan", domain="[('city_id','=',city_id)]")
    kelurahan_id            = fields.Many2one(comodel_name="hr.kelurahan", string="Kelurahan", domain="[('kecamatan_id','=',kecamatan_id)]")
    rt_rw                   = fields.Char(string="RT/RW")
    zip_code                = fields.Char(string="Kode Pos")
    department_id           = fields.Many2one('hr.department', string='Unit Kerja')

    alamat2                 = fields.Char(string="Alamat")
    state_id2               = fields.Many2one(comodel_name="hr.state", string="Provinsi",  domain="[('country_id','=',country_id)]")
    city_id2                = fields.Many2one(comodel_name="hr.city", string="Kota",  domain="[('provinsi_id','=',state_id2)]")
    kecamatan_id2           = fields.Many2one(comodel_name="hr.kecamatan", string="Kecamatan",  domain="[('city_id','=',city_id2)]")
    kelurahan_id2           = fields.Many2one(comodel_name="hr.kelurahan", string="Kelurahan",  domain="[('kecamatan_id','=',kecamatan_id2)]")
    rt_rw2                  = fields.Char(string="RT/RW")
    zip_code2               = fields.Char(string="Kode Pos")

    gol_darah               = fields.Char(string="Golongan Darah")
    warna_kulit             = fields.Char(string="Warna Kulit")
    bentuk_wajah            = fields.Char(string="Bentuk Wajah")
    jenis_rambut            = fields.Char(string="Jenis Rambut")
    tinggi_bb               = fields.Char(string="Tingg dan Berat Badan")

    email_ykp               = fields.Char(string="Email YKP bank bjb")
    email_pribadi           = fields.Char(string="Email Pribadi")
    telepon                 = fields.Integer(string="Telepon")
    handphone1              = fields.Integer(string="Handphone 1")
    handphone2              = fields.Integer(string="Handphone 2")

    name_darurat            = fields.Char(string="Nama")
    hubungan_darurat        = fields.Char(string="Hubungan")
    handphone_darurat       = fields.Char(string="handphone")
    alamat_darurat          = fields.Char(string="Alamat")
    state_id_darurat               = fields.Many2one(comodel_name="hr.state", string="Provinsi",  domain="[('country_id','=',country_id)]")
    city_id_darurat                = fields.Many2one(comodel_name="hr.city", string="Kota",  domain="[('provinsi_id','=',state_id_darurat)]")
    kecamatan_id_darurat           = fields.Many2one(comodel_name="hr.kecamatan", string="Kecamatan",  domain="[('city_id','=',city_id_darurat)]")
    kelurahan_id_darurat           = fields.Many2one(comodel_name="hr.kelurahan", string="Kelurahan",  domain="[('kecamatan_id','=',kecamatan_id_darurat)]")
    rt_rw_darurat                  = fields.Char(string="RT/RW")
    zip_code_darurat               = fields.Char(string="Kode Pos")

    no_bpjs                        = fields.Char(string="Nomor BPJS")
    faskes                         = fields.Char(string="Faskes Tingkat")
    dokter_gigi                    = fields.Char(string="Dokter Gigi")

    hubungan_ayah                  = fields.Selection([('ayah','AYAH')],string='Hubungan',required=True, default='ayah')
    nama_ayah                      = fields.Char(string="nama")
    lahir_ayah                     = fields.Date(string="Tanggal Lahir")
    ktp_ayah                       = fields.Char(string="No KTP-NIK")
    pekerjaan_ayah                 = fields.Char(string="Pekerjaan")
    hubungan_ibu                   = fields.Selection([('ibu','IBU')],string='Hubungan',required=True, default='ibu')
    nama_ibu                       = fields.Char(string="nama")
    lahir_ibu                      = fields.Date(string="Tanggal Lahir")
    ktp_ibu                        = fields.Char(string="No KTP-NIK")
    pekerjaan_ibu                  = fields.Char(string="Pekerjaan")

    nama_pasangan                  = fields.Char(string="Nama")
    ktp_pasangan                   = fields.Char(string="No KTP-NIK")
    tempatlahir_pasangan           = fields.Char(string="Tempat Lahir")
    tanggallahir_pasangan          = fields.Date(string="Tanggal Lahir")
    pekerjaan_pasangan             = fields.Char(string="Pekerjaan")
    statusc_pasangan               = fields.Char(string="Status Cerai")
    statusm_pasangan               = fields.Char(string="Status Meninggal")

    anak1                          = fields.Char(string="Anak Ke")
    nama_anak1                     = fields.Char(string="Nama")
    tempatlahir_anak1              = fields.Char(string="Tempat Lahir")
    tanggallahir_anak1             = fields.Date(string="Tanggal Lahir")
    jeniskelamin_anak1             = fields.Char(string="Jenis Kelamin")
    status_anak1                   = fields.Char(string="Status")
    noakta_anak1                   = fields.Char(string="No Akta")
    anak2                          = fields.Char(string="Anak Ke")
    nama_anak2                     = fields.Char(string="Nama")
    tempatlahir_anak2              = fields.Char(string="Tempat Lahir")
    tanggallahir_anak2             = fields.Date(string="Tanggal Lahir")
    jeniskelamin_anak2             = fields.Char(string="Jenis Kelamin")
    status_anak2                   = fields.Char(string="Status")
    noakta_anak2                   = fields.Char(string="No Akta")

    unit_kerja                     = fields.Many2one(comodel_name="hr.department",string="Unit Kerja")
    penempatan                     = fields.Many2one(comodel_name="hr.department", string="Penempatan")
    jenis_pegawai                  = fields.Many2one(comodel_name="jenis.pegawai", string="Jenis Pegawai")
    masa_jabatan                   = fields.Char(string="Masa Jabatan")
    grade                          = fields.Many2one(comodel_name="hr.grade", string="Grade")
    masa_grade                     = fields.Char(string="Masa Grade")
    tanggal_masuk                  = fields.Date(string="Tanggal Masuk")
    masa_kerja                     = fields.Char(string="Masa Kerja")
    tanggal_pengangkatan           = fields.Date(string="Tanggal Pengangkatan")
    tanggal_pensiun                = fields.Date(string="Tanggal Pensiun")
    tanggal_keluar                 = fields.Date(string="Tanggal Keluar")
    tahun_cuti_besar               = fields.Integer(string="Tahun Cuti Besar")
    no_jamsostek                   = fields.Char(string="Nomor Jamsostek")
    no_npwp                        = fields.Char(string="Nomor NPWP")
    potongan_asuransi_jiwa         = fields.Char(string="Potongan Asuransi Jiwa")
    status_nikah_pajak_TB          = fields.Char(string="Status Nikah Pajak (TB)")
    status_nikah_pajak_TD          = fields.Char(string="Status Nikah Pajak (TD)")
    jum_tanggungan_TB              = fields.Char(string="Jumlah Tanggungan Tahun Berjalan")
    jum_tanggungan_TD              = fields.Char(string="Jumlah Tanggungan Tahun Depan")
    program_karir                  = fields.Char(string="Program Karir")
    status_pegawai                 = fields.Char(string="Status Pegawai")
    education_ids                  = fields.One2many(comodel_name="hr.education", string="Pendidikan", inverse_name="employee_id")
    educationlain_ids              = fields.One2many(comodel_name="hr.education.lain", string="Pendidikan Lainya", inverse_name="employee_id")
    organization_ids               = fields.One2many(comodel_name="hr.organization", string="Organization History", inverse_name="employee_id")
    certification_ids              = fields.One2many(comodel_name="hr.certification", string="Certification", inverse_name="employee_id")
    penghargaan_ids                = fields.One2many(comodel_name="hr.penghargaan", string="Penghargaan", inverse_name="employee_id")
    kursus_ids                     = fields.One2many(comodel_name="hr.training",string="Certification", inverse_name="employee_id")

    mutasi_ids                     = fields.One2many(comodel_name="hr.mutasi", string="Mutasi Kepanhgkatan/Grade", inverse_name="employee_id")
    mutasijbtn_ids                 = fields.One2many(comodel_name="hr.mutasi.jabatan", string="Mutasi Jabatan", inverse_name="employee_id")
    performance_ids                = fields.One2many(comodel_name="hr.work.kpi", string="My Perfromance", inverse_name="name")
    diklat_ids                     = fields.One2many(comodel_name="hr.training.participant", string="Riwayat Diklat", inverse_name="name")
    sanksi_ids                     = fields.One2many(comodel_name="hr.sanksi", string="Sanksi", inverse_name="employee_id")
    orgatasan_ids                  = fields.One2many(comodel_name="hr.orgatasan", string="Atasan", inverse_name="employee_id")
    orgbawahan_ids                 = fields.One2many(comodel_name="hr.orgbawahan", string="Bawahan", inverse_name="employee_id")
    tax_ids                        = fields.One2many(comodel_name="hr.tax", string="My TAX", inverse_name="employee_id")
    luarykp_ids                    = fields.One2many(comodel_name="luar.ykp", string="Di Luar ykp bjb", inverse_name="employee_id")

class Hr_religion(models.Model):
    _name = 'hr.religion'

    name                    = fields.Char(string="Name")

class Hr_state(models.Model):
    _name = 'hr.state'

    name                    = fields.Char(string="Name")
    country_id              = fields.Many2one(string="Negara", required=True, comodel_name="res.country" )

class Hr_city(models.Model):
    _name = 'hr.city'

    name                    = fields.Char(string="Name")
    provinsi_id             = fields.Many2one(string="Provinsi", required=True, comodel_name="hr.state" )

class Hr_kecamatan(models.Model):
    _name = 'hr.kecamatan'

    name                    = fields.Char(string="Name")
    city_id             = fields.Many2one(string="Kota", required=True, comodel_name="hr.city" )

class Hr_kelurahan(models.Model):
    _name = 'hr.kelurahan'

    name                    = fields.Char(string="Name")
    kecamatan_id            = fields.Many2one(string="Kecamatan", required=True, comodel_name="hr.kecamatan" )

class Hr_degree(models.Model):
    _name = 'hr.degree'

    name = fields.Char(string="Name")

class Hr_employee_education_formal(models.Model):
    _name = 'hr.education'

    name  = fields.Many2one(comodel_name="hr.degree", string="Jenjang", required=True)
    kampus = fields.Char(string="Nama Institusi", required=True)
    fakultas = fields.Char(string="Fakultas", required=False)
    jurusan = fields.Char(string="Jurusan", required=False)
    end_year = fields.Char(string="Tahun Lulus", required=False)
    ipk = fields.Char(string="IPK")
    predikat = fields.Char(string="Predikat")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_employee_education_formal(models.Model):
    _name = 'hr.education.lain'

    name  = fields.Char(string="Nama Kursus", required=True)
    penyelenggara = fields.Char(string="Nama Penyelenggara", required=True)
    date_start = fields.Date(string="Tanggal Mulai", required=True)
    date_end = fields.Char(string="Tanggl Berakhir", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_organization(models.Model):
    _name = 'hr.organization'

    name  = fields.Char(string="Nama Organisasi", required=True)
    alamat = fields.Char(string="Alamat Organisasi", required=True)
    start_date = fields.Date(string="Tanggal Mulai", required=True)
    end_date = fields.Date(string="Tanggal Berakhir", required=True)
    position = fields.Char(string="Jabatan Terakhir", required=True)
    honor = fields.Char(string="Honor Terakhir")
    keterangan = fields.Char(string="Keterangan")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_training(models.Model):
    _name = 'hr.training'

    name  = fields.Char(string="Nama Kursus", required=True)
    tempat = fields.Char(string="Tempat", required=True)
    kota = fields.Char(string="Kota")
    penyelenggara = fields.Char(string="Penyelenggara", required=False)
    tanggal_mulai = fields.Date(string="Tanggal Mulai", required=True)
    tanggal_berakhir = fields.Date(string="Tanggal Berakhir")
    nosertifikat = fields.Char(string="No Sertifikat")
    predikat = fields.Char(string="Predikat")
    nilai = fields.Char(string="Nilai")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_certification(models.Model):
    _name = 'hr.certification'

    name  = fields.Char(string="Nama Sertifikasi", required=True)
    lembaga = fields.Char(string="Penyelenggara", required=True)
    date = fields.Date(string="Tanggal", required=True)
    end_date = fields.Date(string="Tanggal Akhir Berlaku", required=True)
    no_sertifikat = fields.Char(string="No Sertifikat", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_penghargaan(models.Model):
    _name = 'hr.penghargaan'

    name  = fields.Char(string="Nama Sertifikasi", required=True)
    lembaga = fields.Char(string="Penyelenggara", required=True)
    date = fields.Date(string="Tanggal", required=True)
    end_date = fields.Date(string="Tanggal Akhir Berlaku")
    no_sertifikat = fields.Char(string="No Sertifikat", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_Grade(models.Model):
    _name = 'hr.grade'

    name = fields.Char(string="Grade")

class Hr_mutasi(models.Model):
    _name = 'hr.mutasi'

    # sebelum_jabatan  = fields.Many2one(comodel_name="hr.job", string="Jabatan Sebelum", required=True)
    # sebelum_grade = fields.Many2one(comodel_name="hr.grade", string="Grade Sebelum", required=True)
    # sesudah_jabatan = fields.Many2one(comodel_name="hr.job", string="Jabatan Sesudah", required=True)
    # sesudah_grade = fields.Many2one(comodel_name="hr.grade", string="Grade Sesudah", required=True)
    sebelum_jabatan  = fields.Char(string="Jabatan Sebelum", required=True)
    sebelum_grade = fields.Char(string="Grade Sebelum", required=True)
    sesudah_jabatan = fields.Char(string="Jabatan Sesudah", required=True)
    sesudah_grade = fields.Char(string="Grade Sesudah", required=True)
    no_sk = fields.Char(string="No SK", required=True)
    tgl_sk = fields.Date(string="Tgl. SK", required=True)
    tgl_efektif = fields.Date(string="Tgl Efektif", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_mutasijabatan(models.Model):
    _name = 'hr.mutasi.jabatan'

    no_sk = fields.Char(string="No SK", required=True)
    tgl_sk = fields.Date(string="Tgl. SK", required=True)
    jenis = fields.Char(string="Jenis", required=True)
    tgl_efektif = fields.Date(string="Tgl Efektif", required=True)
    uk_sebelum  = fields.Many2one(comodel_name="hr.department", string="Unti Kerja Sebelum", required=True)
    grade_sebelum = fields.Many2one(comodel_name="hr.grade", string="Grade Sebelum",required=True)
    jabatan_sebelum = fields.Many2one(comodel_name="hr.job", string="Jabatan Sebelum", required=True)
    uk_sesudah = fields.Many2one(comodel_name="hr.department", string="Unit Kerja Sesudah", required=True)
    grade_sesudah = fields.Many2one(comodel_name="hr.grade", string="Grade Sesudah", required=True)
    jabatan_sesudah = fields.Many2one(comodel_name="hr.job", string="Jabatan Sesudah", required=True)
    penempatan = fields.Char(string="Penempatan")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_performances(models.Model):
    _name = 'hr.performances'

    semester1 = fields.Char(string="Semester I", required=True)
    semester2 = fields.Char(string="Semester II", required=True)
    keterangan = fields.Char(string="Keterangan", required=True)
   
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_diklat(models.Model):
    _name = 'hr.diklat'

    no_surat = fields.Char(string="No Surat", required=True)
    nama_diklat = fields.Char(string="Nama Diklat", required=True)
    tanggal_berangkat = fields.Char(string="Tanggal Berangkat", required=True)
    tanggal_kembali   = fields.Char(string="Tanggal Kembali", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_sanksi(models.Model):
    _name = 'hr.sanksi'

    no_sk = fields.Char(string="No,SKt", required=True)
    keterangan = fields.Char(string="Keterangan", required=True)
    uraian_sanksi = fields.Char(string="Uraian Sanksi", required=True)
    tanggal   = fields.Date(string="Tanggal", required=True)
    tanggal_mulai = fields.Date(string="Tanggal Mulai")
    tanggal_berakhir = fields.Date(string="Tanggal Berakhir")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_orgatasan(models.Model):
    _name = 'hr.orgatasan'

    job_id = fields.Many2one(comodel_name="hr.job", string="Jabatan", required=True)
    nama = fields.Char(string="Nama", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_orgbawahan(models.Model):
    _name = 'hr.orgbawahan'

    job_id = fields.Many2one(comodel_name="hr.job", string="Jabatan", required=True)
    nama = fields.Char(string="Nama", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Hr_tax(models.Model):
    _name = 'hr.tax'

    tahun = fields.Char(string="Tahun")
    job_id = fields.Many2one(comodel_name="hr.job", string="Jabatan", required=True)
    nama_unit = fields.Many2one(comodel_name="hr.department", string="Nama Unit")
    tampilan = fields.Binary(string="Tampilan")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class luar_ykp(models.Model):
    _name = 'luar.ykp'

    name = fields.Char(string="Nama Perusahaan")
    bidang = fields.Char(string="Bidang")
    tahun_masuk = fields.Char(string="Tahun Masuk")
    gaji = fields.Integer(string="Gaji Terakhir")
    job_id = fields.Char(string="Jabatan")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="employee")

class Jenispegawai(models.Model):
    _name = 'jenis.pegawai'

    name = fields.Char(string="Nama")