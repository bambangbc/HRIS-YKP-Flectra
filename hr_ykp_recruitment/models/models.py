# -*- coding: utf-8 -*-

import logging

from flectra import models, fields, api, exceptions

_logger = logging.getLogger(__name__)


class Job(models.Model):
    _inherit = "hr.job"

    stage_survey_ids = fields.One2many('hr.job.stage.survey', 'job_id', string="Daftar Formulir Wawancara")
    work_experience = fields.Integer('Pengalaman Kerja (Thn)')
    min_education = fields.Selection([
        ('d3', 'D3'),
        ('s1', 'S1'),
        ('s2', 'S2')
    ], string='Min Pendidikan')
    jenis_kelamin = fields.Selection([
        ('laki-laki', 'Laki-Laki'),
        ('perempuan', 'Perempuan')
    ])
    usia = fields.Integer('Min Usia', default=0)
    max_usia = fields.Integer('Max Usia', default=0)

    @api.multi
    def action_show_survey(self):
        view = self.env['ir.model.data'].get_object('hr_ykp_recruitment', 'view_job_stage_survey_tree')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Daftar Form Interview',
            'res_model': 'hr.job.stage.survey',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [[view.id, "tree"]],
            'domain': [('job_id', '=', self.id)],
            'target': 'new'
        }


class survey_input(models.Model):
    _inherit = 'survey.user_input'

    job_stage_id = fields.Many2one('hr.recruitment.stage')
    applicant_id = fields.Many2one('hr.applicant')


class job_stage_survey(models.Model):
    _name = 'hr.job.stage.survey'

    job_id = fields.Many2one('hr.job')
    stage_id = fields.Many2one('hr.recruitment.stage')
    survey_id = fields.Many2one(
        'survey.survey', "Interview Form",
        help="Choose an interview form for this job position and you will be able to print/answer this interview from all applicants who apply for this job")


class applicant_interview_score(models.Model):
    _name = 'hr.applicant.score'

    # @api.depends('answer_id')
    # def _compute_score(self):
    #     for row in self:
    #         row.score = row.answer_id.quizz_score

    applicant_id = fields.Many2one('hr.applicant')
    stage_id = fields.Many2one('hr.recruitment.stage')
    answer_id = fields.Many2one('survey.user_input')
    score = fields.Char(store=True)


class Applicant(models.Model):
    _inherit = "hr.applicant"

    @api.depends('work_experience', 'job_work_experience')
    def _compute_matched_work(self):
        for row in self:
            row.matched_work_experience = row.work_experience >= row.job_work_experience

    @api.depends('min_education', 'job_min_education')
    def _compute_matched_education(self):
        for row in self:
            _logger.info('Min Edu : {} Job Min Edu : {}'.format(row.min_education, row.job_min_education))
            if row.job_min_education == 'd3':
                if row.min_education == 'd3' or row.min_education == 's1' or row.min_education == 's2':
                    row.matched_min_education = True
                else:
                    row.matched_min_education = False
            elif row.job_min_education == 's1':
                if row.min_education == 's1' or row.min_education == 's2':
                    row.matched_min_education = True
                else:
                    row.matched_min_education = False
            elif row.job_min_education == 's2':
                if row.min_education == 's2':
                    row.matched_min_education = True
                else:
                    row.matched_min_education = False
            else:
                row.matched_min_education = True

    @api.depends('jenis_kelamin', 'job_jenis_kelamin')
    def _compute_matched_jk(self):
        for row in self:
            _logger.info('Jenis Kelamin : {} Job Jenis Kelamin : {} sama : {} '.format(row.jenis_kelamin, row.job_jenis_kelamin, row.jenis_kelamin == row.job_jenis_kelamin))
            if row.job_jenis_kelamin:
                row.matched_jenis_kelamin = row.jenis_kelamin == row.job_jenis_kelamin
                _logger.info('matched jk : {}'.format(row.matched_jenis_kelamin))
            else:
                row.matched_jenis_kelamin = True

    @api.depends('usia', 'job_usia')
    def _compute_matched_usia(self):
        for row in self:
            _logger.info('Usia : {} Job Usia : {}'.format(row.usia, row.job_usia))
            row.matched_usia = row.usia >= row.job_usia

    @api.depends('usia', 'job_max_usia')
    def _compute_matched_max_usia(self):
        for row in self:
            _logger.info('Max Usia : {} Job Max Usia : {}'.format(row.usia, row.job_max_usia))
            if row.job_max_usia != 0:
                row.matched_max_usia = row.usia <= row.job_max_usia
            else:
                row.matched_max_usia = True

    work_experience = fields.Integer('Pengalaman Kerja (Thn)')
    min_education = fields.Selection([
        ('d3', 'D3'),
        ('s1', 'S1'),
        ('s2', 'S2')
    ], string='Min Pendidikan')
    jenis_kelamin = fields.Selection([
        ('laki-laki', 'Laki-Laki'),
        ('perempuan', 'Perempuan')
    ])
    usia = fields.Integer('Usia', default=0)
    score = fields.Integer('Nilai')
    score_ids = fields.One2many('hr.applicant.score', 'applicant_id', string='Hasil Penilaian')
    job_work_experience = fields.Integer(related='job_id.work_experience', string="syarat Min Pengalaman")
    matched_work_experience = fields.Boolean(compute=_compute_matched_work, string="Syarat Pengalaman Cocok",
                                             store=True, compute_sudo=True)
    job_min_education = fields.Selection(related='job_id.min_education', string="syarat Min Pendidikan")
    matched_min_education = fields.Boolean(compute=_compute_matched_education, string="Syarat Pendidikan Cocok",
                                           store=True, compute_sudo=True)
    job_jenis_kelamin = fields.Selection(related='job_id.jenis_kelamin', string="syarat Jenis Kelamin")
    matched_jenis_kelamin = fields.Boolean(compute=_compute_matched_jk, string="Syarat Jenis Kelamin Cocok",
                                           store=True, compute_sudo=True)
    job_usia = fields.Integer(related='job_id.usia', string="syarat Min Usia")
    matched_usia = fields.Boolean(compute=_compute_matched_usia, string="Syarat Usia Cocok",
                                  store=True, compute_sudo=True)
    job_max_usia = fields.Integer(related='job_id.max_usia', string="syarat Max Usia")
    matched_max_usia = fields.Boolean(compute=_compute_matched_max_usia, string="Syarat Usia Cocok",
                                      store=True, compute_sudo=True)

    @api.model
    def create(self, vals):
        vals['stage_id'] = self.env['hr.recruitment.stage'].search([], limit=1).id
        return super(Applicant, self).create(vals)

    @api.multi
    def action_start_stage_survey(self):
        self.ensure_one()
        stage_id = self.env.context['stage_id']
        job_id = self.env.context['job_id']
        survey_id = self.env['hr.job.stage.survey'].search([('stage_id', '=', stage_id), ('job_id', '=', job_id)],
                                                           limit=1)
        if survey_id.id > 0:
            response = self.env['survey.user_input'].search(
                [('applicant_id', '=', self.id), ('job_stage_id', '=', stage_id)], limit=1)
            if not response.id:
                response = self.env['survey.user_input'].create(
                    {'survey_id': survey_id.survey_id.id, 'applicant_id': self.id, 'job_stage_id': stage_id})
                self.env['hr.applicant.score'].create({
                    'stage_id': stage_id,
                    'applicant_id': self.id,
                    'answer_id': response.id
                })
            # grab the token of the response and start surveying
            return survey_id.survey_id.with_context(survey_token=response.token).action_start_survey()
        else:
            raise exceptions.ValidationError('Tidak ada dokumen wawancara')

    @api.multi
    def action_print_stage_survey(self):
        self.ensure_one()
        stage_id = self.env.context['stage_id']
        job_id = self.env.context['job_id']
        survey_id = self.env['hr.job.stage.survey'].search([('stage_id', '=', stage_id), ('job_id', '=', job_id)],
                                                           limit=1)
        if survey_id.survey_id.id > 0:
            response = self.env['survey.user_input'].search(
                [('survey_id', '=', survey_id.survey_id.id), ('applicant_id', '=', self.id)], limit=1)
            if response:
                return survey_id.survey_id.with_context(survey_token=response.token).action_print_survey()
