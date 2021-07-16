import datetime

from flectra import models, fields, api, exceptions


class survey_department(models.Model):
    _inherit = 'survey.survey'

    survey_department = fields.Boolean('Survey Department ?')
    survey_department_pengurus = fields.Boolean('Survey Department ?')


class survey_department_input_employee(models.Model):
    _inherit = 'survey.user_input'

    semester = fields.Selection([
        ('semester_1', 'Semester 1'),
        ('semester_2', 'Semester 2')
    ], string='Semester', default='semester_1')
    quarter = fields.Selection([
        ('q1', 'Kuartal 1'),
        ('q2', 'Kuartal 2'),
        ('q3', 'Kuartal 3'),
        ('q4', 'Kuartal 4'),
    ], string='Kuartal', default="q1")

    year = fields.Char('Tahun')
    employee_id = fields.Many2one('hr.employee')


class survey_department_input_line_employee(models.Model):
    _inherit = 'survey.user_input_line'

    quarter = fields.Selection(related='user_input_id.quarter', store=True)
    job_id = fields.Many2one(related='user_input_id.employee_id.job_id', store=True)
    survey_department_pengurus = fields.Boolean(related='survey_id.survey_department_pengurus',
                                                string='Survey Department Pengurus ?')


class DepartmentAppraisal(models.Model):
    _name = 'hr.department.appraisal'

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])

    def _default_survey_department(self):
        return self.env['survey.survey'].search([('survey_department', '=', True)], limit=1)

    def _default_survey_department_pengurus(self):
        return self.env['survey.survey'].search([('survey_department_pengurus', '=', True)], limit=1)

    def name_get(self):
        result = []
        for record in self:
            name = 'Appraisal {} {}'.format(record.semester, record.year)
            result.append((record.id, name))
        return result

    semester = fields.Selection([
        ('semester_1', 'Semester 1'),
        ('semester_2', 'Semester 2')
    ], string='Semester', default='semester_1')
    quarter = fields.Selection([
        ('q1', 'Kuartal 1'),
        ('q2', 'Kuartal 2'),
        ('q3', 'Kuartal 3'),
        ('q4', 'Kuartal 4'),
    ], string='Kuartal', default="q1")
    year = fields.Char('Tahun', default=datetime.datetime.now().year)
    employee_id = fields.Many2one('hr.employee', default=_default_employee, string='Karyawan')
    user_id = fields.Many2one(related='employee_id.user_id')
    survey_id = fields.Many2one('survey.survey', domain=[('survey_department', '=', True)],
                                default=_default_survey_department)
    survey_department_pengurus = fields.Boolean(related='survey_id.survey_department_pengurus',
                                                string='Survey Department Pengurus ?')
    answer_id = fields.Many2one('survey.user_input', 'Jawaban')

    @api.model
    def create(self, vals):
        quarter = vals['quarter']
        year = vals['year']
        employee_id = self._default_employee().id
        appraisal = self.env['hr.department.appraisal'].search(
            [('quarter', '=', quarter), ('year', '=', year), ('employee_id', '=', employee_id)], limit=1)
        if appraisal:
            raise exceptions.ValidationError('Penilaian untuk {} dan Tahun {} sudah ada'.format(quarter, year))

        if self.env.user.has_group('hr_ykp_employees.group_hr_pengurus') or self.env.user.has_group(
                'hr_ykp_training.group_pengurus'):
            vals['survey_id'] = self._default_survey_department_pengurus().id
        else:
            vals['survey_id'] = self._default_survey_department().id
        result = super(DepartmentAppraisal, self).create(vals)

        response = self.env['survey.user_input'].create(
            {'survey_id': result.survey_id.id, 'employee_id': result.employee_id.id, 'quarter': result.quarter,
             'year': result.year})
        result.write({'answer_id': response.id})
        result.survey_id.response_ids = [(6, 0, [response.id])]
        return result

    @api.multi
    def action_start_stage_survey(self):
        self.ensure_one()
        if self.survey_id and self.employee_id:
            response = self.env['survey.user_input'].search([('employee_id', '=', self.employee_id.id)], limit=1)
            if not response.id:
                response = self.env['survey.user_input'].create(
                    {'survey_id': self.survey_id.id, 'employee_id': self.employee_id.id, 'quarter': self.quarter,
                     'year': self.year})
                self.survey_id.response_ids = [(6, 0, [response.id])]
            # grab the token of the response and start surveying
            return self.survey_id.with_context(survey_token=response.token).action_start_survey()


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    value_suggested = fields.Many2one('survey.label', string="Suggested answer", group_operator='max')
    quizz_mark = fields.Float('Skor', digits=(12, 2), group_operator='avg')
    employee_id = fields.Many2one(related='user_input_id.employee_id', store=True)
    page_id = fields.Many2one(related='question_id.page_id', string="Page", store=True)
