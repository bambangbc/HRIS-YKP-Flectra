# -*- coding: utf-8 -*-
import datetime
import locale

from flectra import models, fields, api

locale.setlocale(locale.LC_ALL, '')


class res_partner(models.Model):
    _inherit = 'res.partner'

    is_instructure = fields.Boolean('Instruktur ?')


class employee(models.Model):
    _inherit = 'hr.employee'

    training_participant_ids = fields.One2many('hr.training.participant', 'name', string='Pelatihan diikuti',
                                               domain=[('state', '=', 'approve')])


class Hr_state(models.Model):
    _name = 'hr.state'

    name = fields.Char(string="Name")
    country_id = fields.Many2one(string="Negara", required=True, comodel_name="res.country")


class Hr_city(models.Model):
    _name = 'hr.city'

    name = fields.Char(string="Name")
    provinsi_id = fields.Many2one(string="Provinsi", required=True, comodel_name="hr.state")


class training_course(models.Model):
    _name = 'hr.training.course'

    def _default_template(self):
        data = [
            (0, 0, {
                'name': 'Behavioral',
                'bobot': 20
            }),
            (0, 0, {
                'name': 'Formative Test',
                'bobot': 80
            })
        ]
        return data

    def generate_scoring(self):
        self.evaluation_ids.unlink()
        self.write({'evaluation_ids': self._default_template()})

    name = fields.Char('Nama Pelatihan')
    type = fields.Selection([
        ('in_house', 'In House Training'),
        ('public', 'Public Training'),
    ], string='Jenis Pelatihan')
    desc = fields.Html('Maksud dan Tujuan')
    evaluation_ids = fields.One2many('hr.training.course.evaluation', 'course_id',
                                     string="Template Evaluasi", default=_default_template)


class training_course_evaluation(models.Model):
    _name = 'hr.training.course.evaluation'

    name = fields.Char('Item Penilaian')
    bobot = fields.Integer('Bobot Penilaian (%)')
    course_id = fields.Many2one('hr.training.course')


class hr_training_request(models.Model):
    _name = 'hr.training.request'

    def _get_default_employee(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        return employee

    @api.onchange('start_date', 'end_date')
    def _compute_duratiom(self):
        for row in self:
            if row.start_date and row.end_date:
                DATETIME_FORMAT = "%Y-%m-%d"
                from_dt = datetime.datetime.strptime(row.start_date, DATETIME_FORMAT)
                to_dt = datetime.datetime.strptime(row.end_date, DATETIME_FORMAT)
                timedelta = to_dt - from_dt
                diff_day = timedelta.days + 1
                row.duration = diff_day

    @api.onchange('type')
    def onchange_instructure(self):
        if self.type == 'public':
            self.external_instructure = True
        else:
            self.external_instructure = False

    def _default_negara_tujuan(self):
        return self.env['res.country'].search([('id', '=', 100)], limit=1)

    name = fields.Many2one('hr.training.course', string='Pelatihan')
    desc = fields.Html(related='name.desc', string='Maksud dan Tujuan')
    type = fields.Selection(related='name.type', string='Jenis Pelatihan')
    pola_ajuan = fields.Selection([
        ('ajuan_karyawan', 'Dari Karyawan / Unit Kerja'),
        ('penugasan', 'Penugasan'),
    ], default='ajuan_karyawan', string="Pola Ajuan Pelatihan")
    location = fields.Char('Lokasi Pelatihan')
    start_date = fields.Date('Tanggal Mulai')
    end_date = fields.Date('Tanggal Selesai')
    duration = fields.Integer()
    city_start = fields.Char('Kota Keberangkatan')
    city_destination = fields.Char('Kota Tujuan')
    negara_tujuan = fields.Many2one('res.country', string="Negara Tujuan", default=_default_negara_tujuan)
    propinsi_tujuan = fields.Many2one("hr.state", string="Propinsi Tujuan")
    tempat_tujuan = fields.Many2one("hr.city", string="Kota Tujuan")
    participant_ids = fields.One2many('hr.training.participant', 'request_id', string="Ajuan Peserta")
    external_instructure = fields.Boolean('Instruktur Eksternal ?')
    instructure_id = fields.Many2one('res.partner', string="Instruktur", domain=[('is_instructure', '=', True)])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_hr', 'Pending Bag SDM'),
        ('pending', 'Pending Pengurus / Pembina'),
        ('approve', 'Disetujui'),
        ('decline', 'Ditolak')
    ], default='draft')
    document_ids = fields.One2many('hr.training.request.document', 'request_id', string="Dokumen pendukung")
    training_cost = fields.Float('Biaya Investasi')
    unit_request = fields.Selection([
        ('hr', 'Bagian SDM'),
        ('department', 'Unit Kerja'),
        ('employee', 'Karyawan'),
        ('pengurus', 'Pengurus'),
    ], string='Jenis Memo Ajuan', default='employee')
    department_id = fields.Many2one('hr.department', string="Department")
    employee_id = fields.Many2one('hr.employee', string="Karyawan", default=_get_default_employee)
    user_id = fields.Many2one(related='employee_id.user_id')
    notes = fields.Html('Keterangan')

    def _get_al_number(self):
        return self.env['ir.sequence'].get('seq.training.assignment')

    @api.multi
    def action_pending_hr(self):
        self.write({'state': 'pending_hr'})

    @api.multi
    def action_pending(self):
        self.write({'state': 'pending'})

    def _generate_assigment_letter(self, al_number, employee_name):
        if self.type == 'in_house':
            tpl = self.env['hr.training.cfg.assignment.letter'].sudo().search([('name', '=', 'in_house')],
                                                                              limit=1).document
        else:
            tpl = self.env['hr.training.cfg.assignment.letter'].sudo().search([('name', '=', 'public')],
                                                                              limit=1).document
        tpl = tpl.replace("#NOMOR#", str(al_number))
        tpl = tpl.replace("#NAMA_PELATIHAN#", self.name.name)
        tpl = tpl.replace("#TGL_PELATIHAN#", self.start_date)
        tpl = tpl.replace("#WKT_PELATIHAN#", self.start_date)
        tpl = tpl.replace("#TEMPAT#", self.location)
        tpl = tpl.replace("#NAMA_PEGAWAI#", employee_name)
        return tpl

    @api.multi
    def action_approve(self):
        self.write({'state': 'approve'})
        found = False
        for participant in self.participant_ids:
            data = {'state': 'pending'}
            al_number = self._get_al_number() if self.pola_ajuan == 'penugasan' else ''
            if self.employee_id.id == participant.name.id:
                found = True
            data['assignment_letter_number'] = al_number,
            data['assignment_letter'] = self._generate_assigment_letter(al_number, participant.name.name)
            participant.write(data)
        if self.employee_id.id and not found:
            al_number = self._get_al_number() if self.pola_ajuan == 'penugasan' else ''
            self.env['hr.training.participant'].create({
                'name': self.employee_id.id,
                'state': 'pending',
                'request_id': self.id,
                'assignment_letter_number': al_number,
                'assignment_letter': self._generate_assigment_letter(al_number, self.employee_id.name)
            })

    def generate_assignment_letter(self):
        for participant in self.participant_ids:
            data = {}
            if self.pola_ajuan == 'penugasan':
                data['assignment_letter'] = self._generate_assigment_letter(participant.assignment_letter_number,
                                                                            participant.name.name)
            participant.write(data)

    @api.multi
    def action_decline(self):
        self.write({'state': 'decline'})

    @api.model
    def create(self, vals):
        if (vals.get('start_date') and vals.get('end_date')):
            DATETIME_FORMAT = "%Y-%m-%d"
            from_dt = datetime.datetime.strptime(vals['start_date'], DATETIME_FORMAT)
            to_dt = datetime.datetime.strptime(vals['end_date'], DATETIME_FORMAT)
            timedelta = to_dt - from_dt
            diff_day = timedelta.days + 1
            vals['duration'] = diff_day
        rec = super(hr_training_request, self).create(vals)
        return rec


class hr_training_request_document(models.Model):
    _name = 'hr.training.request.document'

    name = fields.Selection([
        ('brosur', 'Brosur'),
        ('offering_letter', 'Surat Penawaran'),
        ('tor', 'TOR'),
        ('rab', 'RAB'),
        ('other', 'Lainnya')
    ], string='Jenis Dokumen')
    document = fields.Binary('Dokumen')
    filename = fields.Char('Nama File')
    request_id = fields.Many2one('hr.training.request')


class hr_training_participant(models.Model):
    _name = 'hr.training.participant'

    name = fields.Many2one('hr.employee', string="Karyawan")
    user_id = fields.Many2one(related='name.user_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approve', 'Mengikuti'),
        ('decline', 'Tidak Mengikuti')
    ], string='Status', default='draft')
    assignment_letter_number = fields.Char('Nomor Surat Tugas')
    assignment_letter = fields.Html('Surat Tugas')
    request_id = fields.Many2one('hr.training.request', string="Nama Pelatihan")
    type = fields.Selection(related='request_id.type', string='Jenis Pelatihan')
    location = fields.Char(related="request_id.location")
    start_date = fields.Date(related="request_id.start_date")
    end_date = fields.Date(related="request_id.end_date")
    uang_pelatihan = fields.Float('Uang Pelatihan', digits=(12, 0))
    total_uang_pelatihan = fields.Float('Uang Pelatihan', digits=(12, 0))
    pelatihan_cashed = fields.Selection([
        (1, 'Iya'),
        (0, 'Belum')
    ], 'Dicairkan ?', default=0, group_operator='max')

    def action_approve(self):
        self.write({'state': 'approve'})

    def action_decline(self):
        self.write({'state': 'decline'})

    @api.model
    def create(self, vals):
        rec = super(hr_training_participant, self).create(vals)
        if rec.request_id.type == 'public':
            self._create_evalutation(rec.id)
            self._create_vendor_evaluation(rec.id)
        return rec

    def _create_evalutation(self, id):
        evaluation = self.env['hr.training.evaluation'].search([('name', '=', id)], limit=1)
        if not evaluation:
            create_data = {
                'name': id,
                'evaluation_date': fields.Date.context_today(self)
            }
            evaluation = self.env['hr.training.evaluation'].create(create_data)
        return evaluation

    def create_evaluation(self):
        evaluation = self._create_evalutation(self.id)
        view = self.env['ir.model.data'].get_object('hr_ykp_training', 'hr_training_evaluation_form_popup')
        return {
            'type': 'ir.actions.act_window',
            'name': 'From Penilaian',
            'res_model': 'hr.training.evaluation',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [[view.id, "form"]],
            'target': 'new',
            'res_id': evaluation.id
        }

    def _create_vendor_evaluation(self, id):
        evaluation = self.env['hr.training.evaluation.vendor'].search([('name', '=', id)], limit=1)
        if evaluation:
            create_data = {
                'name': id,
                'evaluation_date': fields.Date.context_today(self)
            }
            evaluation = self.env['hr.training.evaluation'].create(create_data)
        else:
            evaluation.evaluation_detail_ids.unlink()
        return evaluation

    def create_vendor_evaluation(self):
        evaluation = self._create_vendor_evaluation(self.id)
        view = self.env['ir.model.data'].get_object('hr_ykp_training', 'hr_training_evaluation_vendor_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'From Penilaian',
            'res_model': 'hr.training.evaluation.vendor',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [[view.id, "form"]],
            'target': 'new',
            'res_id': evaluation.id
        }

    def download_assignment_letter(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=hr.training.participant&id=%s&filename=%s.pdf' % (
                self.id, self.assignment_letter_number),
            'target': 'self',
        }


class hr_training_inhouse_evaluation(models.Model):
    _name = 'hr.training.inhouse.evaluation'

    @api.onchange('name')
    def onchange_name(self):
        details = []
        for ev in self.name.participant_ids:
            if ev.state == 'approve':
                details.append((0, 0, {'name': ev.id}))
        self.evaluation_detail_ids = details

    def calculate_uang_pelatihan(self):
        for ev in self.evaluation_detail_ids:
            jenis_pegawai = ev.name.name.jenis_pegawai
            propinsi_tujuan = ev.name.request_id.propinsi_tujuan
            negara_tujuan = ev.name.request_id.negara_tujuan
            allowance = self.env['hr.perdin.allowance'].search([('jenis_pegawai', '=', jenis_pegawai.id)], limit=1)
            if allowance:
                exclude = False
                for excluded in allowance.location_exclude_ids:
                    if excluded.id == propinsi_tujuan.id:
                        exclude = True
                        break
                if not exclude and negara_tujuan.id == 100:
                    if 'jawa timur' in propinsi_tujuan.name.lower() or 'jawa tengah' in propinsi_tujuan.name.lower():
                        extra = allowance.extra_jawa / 100
                        ev.name.write({
                            'uang_pelatihan': (extra * allowance.nominal) + allowance.nominal,
                            'total_uang_pelatihan': ev.name.request_id.duration * ev.name.uang_pelatihan
                        })
                    else:
                        extra = allowance.extra / 100
                        ev.name.write({
                            'uang_pelatihan': (extra * allowance.nominal) + allowance.nominal,
                            'total_uang_pelatihan': ev.name.request_id.duration * ev.name.uang_pelatihan
                        })
                elif exclude and negara_tujuan.id == 100:
                    ev.name.write({
                        'uang_pelatihan': 125000,
                        'total_uang_pelatihan': ev.name.request_id.duration * ev.name.uang_pelatihan
                    })
                elif negara_tujuan.id != 100:
                    ev.name.write({
                        'uang_pelatihan': allowance.nominal_luar,
                        'total_uang_pelatihan': ev.name.request_id.duration * ev.name.uang_pelatihan
                    })

    name = fields.Many2one('hr.training.request', domain=[('type', '=', 'in_house')])
    type = fields.Selection(related='name.type', store=True)
    evaluation_date = fields.Date('Tanggal Evaluasi')
    evaluation_detail_ids = fields.One2many('hr.training.inhouse.evaluation.detail', 'evaluation_id')

    @api.model
    def create(self, vals):
        rec = super(hr_training_inhouse_evaluation, self).create(vals)
        rec.calculate_uang_pelatihan()
        return rec


class hr_training_inhouse_evaluation_detail(models.Model):
    _name = 'hr.training.inhouse.evaluation.detail'

    @api.onchange('behavioral_score')
    def onchange_behavioral(self):
        self.total_behavioral = self.behavioral_score * 0.2
        self.total_score = self.total_behavioral + self.total_formative

    @api.onchange('formative_score')
    def onchange_formative(self):
        self.total_formative = self.formative_score * 0.8
        self.total_score = self.total_behavioral + self.total_formative

    name = fields.Many2one('hr.training.participant')
    behavioral_score = fields.Float('Behavioral', default=0)
    total_behavioral = fields.Float('Total Behavioral', default=0)
    formative_score = fields.Float('Formative', default=0)
    total_formative = fields.Float('Total Formative', default=0)
    total_score = fields.Float('Total Score', default=0)
    evaluation_id = fields.Many2one('hr.training.inhouse.evaluation')

    @api.model
    def create(self, vals):
        vals['total_behavioral'] = vals.get('behavioral_score', 0) * 0.2
        vals['total_formative'] = vals.get('formative_score', 0) * 0.8
        vals['total_score'] = vals.get('total_behavioral', 0) + vals.get('total_formative', 0)
        return super(hr_training_inhouse_evaluation_detail, self).create(vals)


class hr_training_public_evaluation(models.Model):
    _name = 'hr.training.evaluation'

    def name_get(self):
        result = []
        for record in self:
            name = record.name if record.name.name else record.request_id.name.name
            result.append((record.id, name))
        return result

    name = fields.Many2one('hr.training.participant')
    request_id = fields.Many2one(related='name.request_id', store=True)
    type = fields.Selection(related='request_id.type', store=True)
    evaluation_date = fields.Date('Tanggal Evaluasi')
    evaluation_document = fields.Binary('Dokumen Evaluasi')
    filename = fields.Char('filename')

    def calculate_uang_pelatihan(self):
        jenis_pegawai = self.name.name.jenis_pegawai
        propinsi_tujuan = self.name.request_id.propinsi_tujuan
        negara_tujuan = self.name.request_id.negara_tujuan
        allowance = self.env['hr.perdin.allowance'].search([('jenis_pegawai', '=', jenis_pegawai.id)], limit=1)
        if allowance:
            exclude = False
            for excluded in allowance.location_exclude_ids:
                if excluded.id == propinsi_tujuan.id:
                    exclude = True
                    break
            if not exclude and negara_tujuan.id == 100:
                if 'jawa timur' in propinsi_tujuan.name.lower() or 'jawa tengah' in propinsi_tujuan.name.lower():
                    extra = allowance.extra_jawa / 100
                    self.name.write({
                        'uang_pelatihan': (extra * allowance.nominal) + allowance.nominal,
                        'total_uang_pelatihan': self.name.request_id.duration * self.name.uang_pelatihan
                    })
                else:
                    extra = allowance.extra / 100
                    self.name.write({
                        'uang_pelatihan': (extra * allowance.nominal) + allowance.nominal,
                        'total_uang_pelatihan': self.name.request_id.duration * self.name.uang_pelatihan
                    })
            elif exclude and negara_tujuan.id == 100:
                self.name.write({
                    'uang_pelatihan': 125000,
                    'total_uang_pelatihan': self.name.request_id.duration * self.name.uang_pelatihan
                })
            elif negara_tujuan.id != 100:
                self.name.write({
                    'uang_pelatihan': allowance.nominal_luar,
                    'total_uang_pelatihan': self.name.request_id.duration * self.name.uang_pelatihan
                })

    @api.model
    def create(self, vals):
        rec = super(hr_training_public_evaluation, self).create(vals)
        rec.calculate_uang_pelatihan()
        return rec


class hr_training_evaluation_vendor(models.Model):
    _name = 'hr.training.evaluation.vendor'

    name = fields.Many2one('hr.training.participant')
    request_id = fields.Many2one(related='name.request_id')
    instructure_id = fields.Many2one(related='request_id.instructure_id')
    evaluation_date = fields.Date('Tanggal Evaluasi')
    evaluation_detail_ids = fields.One2many('hr.training.evaluation.vendor.detail', 'evaluation_id',
                                            string="Formulir Evaluasi")
    evaluation_document = fields.Binary('Dokumen Evaluasi')
    filename = fields.Char('filename')


class hr_training_evaluation_vendor_detail(models.Model):
    _name = 'hr.training.evaluation.vendor.detail'

    name = fields.Char('Item Penilaian')
    score = fields.Float('Skor Nilai')
    evaluation_id = fields.Many2one('hr.training.evaluation.vendor')


class hr_training_cfg_letter_job(models.Model):
    _name = 'hr.training.cfg.assignment.letter'

    name = fields.Selection([
        ('in_house', 'In House Training'),
        ('public', 'Public Training'),
    ], string='Jenis Pelatihan')
    document = fields.Html('Template Surat Tugas')
