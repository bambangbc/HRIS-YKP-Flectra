import math

from flectra import _
from flectra import api, fields, models
from flectra.exceptions import UserError


class HolidaysType(models.Model):
    _inherit = "hr.holidays.status"

    type = fields.Selection([
        ('cuti', 'Cuti'),
        ('perdin', 'Perjalanan Dinas'),
        ('izin', "Izin")
    ], string='Type')


class IjinJam(models.Model):
    _name = 'hr.holidays.jam'

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1)

    first_approver_id = fields.Many2one(comodel_name="hr.employee", string="Approve 1")
    second_approver_id = fields.Many2one(comodel_name="hr.employee", string="Approve 2")

    name = fields.Char('Keterangan Ijin')
    employee_id = fields.Many2one('hr.employee', string='Employee', index=True, readonly=True,
                                  states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                  default=_default_employee, track_visibility='onchange')
    jam_mulai = fields.Float('Jam Mulai', readonly=True, index=True, copy=False,
                             states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                             track_visibility='onchange')
    jam_selesai = fields.Float('End Date', readonly=True, copy=False,
                               states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                               track_visibility='onchange')
    double_validation = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
    ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='confirm',
        help="The status is set to 'To Submit', when a leave request is created." +
             "\nThe status is 'To Approve', when leave request is confirmed by user." +
             "\nThe status is 'Refused', when leave request is refused by manager." +
             "\nThe status is 'Approved', when leave request is approved by manager.")

    @api.multi
    def action_confirm(self):
        if self.filtered(lambda holiday: holiday.state != 'draft'):
            raise UserError(_('Leave request must be in Draft state ("To Submit") in order to confirm it.'))
        return self.write({'state': 'confirm'})

    @api.multi
    def action_approve(self):
        # if double_validation: this method is the first approval approval
        # if not double_validation: this method calls action_validate() below
        # self._check_security_action_approve(
        for holidays in self:
            if holidays.env.uid == 1:
                if holidays.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                    current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                    for holiday in self:
                        if holiday.state != 'confirm':
                            raise UserError(_('Leave request must be confirmed ("To Approve") in order to approve it.'))

                        if holiday.double_validation:
                            return holiday.write({'state': 'validate1', 'first_approver_id': current_employee.id})
                        else:
                            holiday.action_validate()
                else:
                    raise UserError(_('Hanya HR Manager Yang Bisa Approve Ini.'))
            else:
                if holidays.first_approver_id.user_id.id == holidays.env.uid or holidays.env.uid == 1:
                    current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                    for holiday in self:
                        if holiday.state != 'confirm':
                            raise UserError(_('Leave request must be confirmed ("To Approve") in order to approve it.'))

                        if holiday.double_validation:
                            return holiday.write({'state': 'validate1', 'first_approver_id': current_employee.id})
                        else:
                            holiday.action_validate()
                else:
                    raise UserError(_('Anda Tidak Memiliki Hak Akses INI.'))

    @api.multi
    def action_validate(self):
        for holidays in self:
            if holidays.env.uid == 1:
                if holidays.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                    current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                    for holiday in self:
                        holiday.write({'state': 'validate'})
                        if holiday.double_validation:
                            holiday.write({'second_approver_id': current_employee.id})
                        else:
                            holiday.write({'first_approver_id': current_employee.id})
                else:
                    raise UserError(_('Hanya HR Manager Yang Bisa Approve Ini.'))
            else:
                if holidays.second_approver_id.user_id.id == holidays.env.uid or holidays.env.uid == 1:
                    current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                    for holiday in self:
                        holiday.write({'state': 'validate'})
                        if holiday.double_validation:
                            holiday.write({'second_approver_id': current_employee.id})
                        else:
                            holiday.write({'first_approver_id': current_employee.id})
                else:
                    raise UserError(_('Anda Tidak Memiliki Hak Akses INI.'))
            return True

    @api.multi
    def action_draft(self):
        if self.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
            for holiday in self:
                if holiday.state not in ['confirm', 'refuse']:
                    raise UserError(
                        _('Leave request state must be "Refused" or "To Approve" in order to reset to Draft.'))
                holiday.write({
                    'state': 'draft',
                    'first_approver_id': False,
                    'second_approver_id': False,
                })
            return True
        else:
            raise UserError(_('Hanya HR Manager Yang Bisa Mengembalikan Ke Draft.'))

    @api.multi
    def action_refuse(self):
        for holidays in self:
            if holidays.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                for holiday in self:
                    if holiday.state not in ['confirm', 'validate', 'validate1']:
                        raise UserError(_('Leave request must be confirmed or validated in order to refuse it.'))

                    if holiday.state == 'validate1':
                        holiday.write({'state': 'refuse', 'first_approver_id': current_employee.id})
                    else:
                        holiday.write({'state': 'refuse', 'second_approver_id': current_employee.id})
                return True
            else:
                raise UserError(_('Hanya HR Manager Yang Bisa Refuse Ini.'))


class Holidays(models.Model):
    _inherit = "hr.holidays"

    approve1 = fields.Many2one(comodel_name="res.users", string="Approve 1")
    approve2 = fields.Many2one(comodel_name="res.users", string="Approve 2")
    type = fields.Selection([
        ('remove', 'Leave Request'),
        ('add', 'Allocation Request'),
        ('perdin', 'Perjalanan Dinas'),
        ('izin', "Izin")
    ], string='Request Type', required=True, readonly=True, index=True, track_visibility='always', default='remove',
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
        help="Choose 'Leave Request' if someone wants to take an off-day. "
             "\nChoose 'Allocation Request' if you want to increase the number of leaves available for someone")
    type2 = fields.Selection([
        ('cuti', 'Cuti'),
        ('perdin', 'Perjalanan Dinas'),
        ('izin', "Izin")
    ], string='Type')
    name = fields.Char('Alasan Cuti')
    tunj_cuti = fields.Boolean('Tunjangan Cuti')
    nomor = fields.Char(string="Nomor Perdin")
    pejabat_berwenang = fields.Many2one(comodel_name="hr.employee", string="Pejabat Berwenang")
    jabatan = fields.Many2one(comodel_name="hr.job", string="Jabatan")
    jabatan_pegawai = fields.Many2one(comodel_name="hr.job", string="Jabatan")
    tempat_berangkat = fields.Many2one(comodel_name="hr.city", string="Tempat Berangkat")
    tempat_tujuan = fields.Many2one(comodel_name="hr.city", string="Tempat Tujuan")
    angkutan = fields.Char(string="Alat angkutan yang di gunakan")
    penanggung_fasilitas = fields.Char(string="Penanggung Fasilitas Perjalanan Dinas")
    datang_di = fields.Char(string="Datang Di")
    tanggal = fields.Date(string="Tanggal")
    date_from = fields.Date('Start Date', readonly=True, index=True, copy=False,
                            states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                            track_visibility='onchange')
    date_to = fields.Date('End Date', readonly=True, copy=False,
                          states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                          track_visibility='onchange')
    jam_selesai = fields.Float('End Date', readonly=True, copy=False,
                               states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                               track_visibility='onchange')
    pengurangan = fields.Boolean(string="Pengurangan")
    holiday_status_id = fields.Many2one("hr.holidays.status", string="Leave Type", required=True, readonly=True,
                                        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                        domain="[('type','=',type2)]")
    tujuan_perdin = fields.Char(string="Tujuan Perdin")
    jenis_perdin = fields.Selection([
        ('collecting', 'Collecting'),
        ('reguler', 'Reguler'),
    ], string='Jenis')
    unti_kerja_penyelenggara = fields.Char("Unit Kerja Penyelenggara")
    cost_centre = fields.Char("Cost Centre")
    perdin_undangan = fields.Boolean("Perdin Undangan")

    max_leaves = fields.Float(compute='_compute_leaves', string='Maximum Allowed',
                              help='This value is given by the sum of all leaves requests with a positive value.')
    leaves_taken = fields.Float(compute='_compute_leaves', string='Leaves Already Taken',
                                help='This value is given by the sum of all leaves requests with a negative value.')
    remaining_leaves = fields.Float(compute='_compute_leaves', string='Remaining Leaves',
                                    help='Maximum Leaves Allowed - Leaves Already Taken')
    virtual_remaining_leaves = fields.Float(compute='_compute_leaves', string='Virtual Remaining Leaves',
                                            help='Maximum Leaves Allowed - Leaves Already Taken - Leaves Waiting Approval')

    _sql_constraints = [
        ('type_value',
         "CHECK( (holiday_type='employee' AND employee_id IS NOT NULL) or (holiday_type='category' AND category_id IS NOT NULL))",
         "The employee or employee category of this request is missing. Please make sure that your user login is linked to an employee."),
        ('date_check2', "CHECK ( (type='add') OR (date_from <= date_to))",
         "The start date must be anterior to the end date."),
        ('date_check', "CHECK ( number_of_days_temp != 0 )", "The number of days must be greater than 0."),
    ]

    def get_days(self):
        result = {self.holiday_status_id.id: dict(max_leaves=0, leaves_taken=0, remaining_leaves=0,
                                                  virtual_remaining_leaves=0)}

        holidays = self.env['hr.holidays'].search([
            ('employee_id', '=', self.employee_id.id),
            ('state', 'in', ['confirm', 'validate1', 'validate']),
            ('holiday_status_id', '=', self.holiday_status_id.id)
        ])

        for holiday in holidays:
            status_dict = result[holiday.holiday_status_id.id]
            if holiday.type == 'add':
                if holiday.state == 'validate':
                    # note: add only validated allocation even for the virtual
                    # count; otherwise pending then refused allocation allow
                    # the employee to create more leaves than possible
                    status_dict['virtual_remaining_leaves'] += holiday.number_of_days_temp
                    status_dict['max_leaves'] += holiday.number_of_days_temp
                    status_dict['remaining_leaves'] += holiday.number_of_days_temp
            elif holiday.type == 'remove':  # number of days is negative
                status_dict['virtual_remaining_leaves'] -= holiday.number_of_days_temp
                if holiday.state == 'validate':
                    status_dict['leaves_taken'] += holiday.number_of_days_temp
                    status_dict['remaining_leaves'] -= holiday.number_of_days_temp
        return result

    @api.multi
    def _compute_leaves(self):
        data_days = self.get_days()
        result = data_days.get(self.holiday_status_id.id, {})
        self.max_leaves = result.get('max_leaves', 0)
        self.leaves_taken = result.get('leaves_taken', 0) - (self.number_of_days if self.state == 'approve' else 0)
        self.remaining_leaves = result.get('remaining_leaves', 0) + (
            self.number_of_days if self.state == 'approve' else 0)
        self.virtual_remaining_leaves = result.get('virtual_remaining_leaves', 0)

    def _get_number_of_days(self, date_from, date_to, employee_id):
        """ Returns a float equals to the timedelta between two dates given as string."""
        # import pdb;pdb.set_trace()
        from_dt = fields.Datetime.from_string(date_from)
        to_dt = fields.Datetime.from_string(date_to)

        if employee_id:
            employee = self.env['hr.employee'].browse(employee_id)
            return employee.get_work_days_count(from_dt, to_dt)

        time_delta = to_dt - from_dt
        return math.ceil(time_delta.days + float(time_delta.seconds) / 86400)

    def hapus_alokasi(self):
        employee_id = self.env['hr.employee'].search([])
        holiday = self.env['hr.holidays'].search([('name', '=', 'Cuti Tahunan')], limit=1)
        if not holiday:
            hol = False
        else:
            hol = holiday
        for emp in employee_id:
            leaves = self.env['hr.holidays'].read_group([
                ('employee_id', 'in', emp.ids),
                ('holiday_status_id.limit', '=', False),
                ('state', '=', 'validate')
            ], fields=['number_of_days', 'employee_id'], groupby=['employee_id'])
            mapping = dict([(leave['employee_id'][0], leave['number_of_days']) for leave in leaves])
            # shift_exist = self.env['hr.rolling.shift.detail'].search([('date_start','<=',str(datetime.now())[:10]),('date_end','>=',str(datetime.now())[:10])])

            if mapping:
                if int(leaves[0]['number_of_days']) > 12:
                    hol_id = {
                        'name': 'alokasi cuti tidak terpakai tahun',
                        'holiday_status_id': 1,
                        'number_of_days_temp': 12 - int(leaves[0]['number_of_days']),
                        'holiday_type': 'employee',
                        'employee_id': emp.id,
                        'department_id': emp.unit_kerja.id,
                        'type': 'add',
                        'state': 'validate',

                    }
                    # import pdb;pdb.set_trace()
                    self.env['hr.holidays'].create(hol_id)
        return True

    @api.onchange('type')
    def _get_type(self):
        if self.type == 'remove' or self.type == 'add':
            id = self.env['hr.holidays.status'].search([('name', '=', 'Cuti Tahunan')], limit=1)

            self.holiday_status_id = id.id
            self.type2 = 'cuti'
        elif self.type == 'perdin':
            id = self.env['hr.holidays.status'].search([('name', '=', 'Perjalanan Dinas')])
            self.holiday_status_id = id.id
            self.type2 = 'perdin'
        elif self.type == 'izin':
            id = self.env['hr.holidays.status'].search([('name', '=', 'KHITAN ANAK')])
            self.holiday_status_id = id.id
            self.type2 = 'izin'

    @api.onchange('pejabat_berwenang')
    def _job_berwenang(self):
        self.jabatan = self.pejabat_berwenang.job_id

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        self.manager_id = self.employee_id and self.employee_id.parent_id
        self.department_id = self.employee_id.department_id
        self.jabatan_pegawai = self.employee_id.job_id

    @api.multi
    def action_approve(self):
        # if double_validation: this method is the first approval approval
        # if not double_validation: this method calls action_validate() below
        # self._check_security_action_approve(
        for holidays in self:
            if holidays.type == 'add' or holidays.env.uid == 1:
                if holidays.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                    current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                    for holiday in self:
                        if holiday.state != 'confirm':
                            raise UserError(_('Leave request must be confirmed ("To Approve") in order to approve it.'))

                        if holiday.double_validation:
                            return holiday.write({'state': 'validate1', 'first_approver_id': current_employee.id})
                        else:
                            holiday.action_validate()
                else:
                    raise UserError(_('Hanya HR Manager Yang Bisa Approve Ini.'))
            else:
                if holidays.approve1.id == holidays.env.uid or holidays.env.uid == 1:
                    current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                    for holiday in self:
                        if holiday.state != 'confirm':
                            raise UserError(_('Leave request must be confirmed ("To Approve") in order to approve it.'))

                        if holiday.double_validation:
                            return holiday.write({'state': 'validate1', 'first_approver_id': current_employee.id})
                        else:
                            holiday.action_validate()
                else:
                    raise UserError(_('Anda Tidak Memiliki Hak Akses INI.'))

    @api.multi
    def action_validate(self):
        for holidays in self:
            if holidays.type == 'add' or holidays.env.uid == 1:
                if holidays.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                    current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                    for holiday in self:
                        # if holiday.state not in ['confirm', 'validate1']:
                        #	raise UserError(_('Leave request must be confirmed in order to approve it.'))
                        # if holiday.state == 'validate1' and not holiday.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                        #	raise UserError(_('Only an HR Manager can apply the second approval on leave requests.'))

                        holiday.write({'state': 'validate'})
                        if holiday.double_validation:
                            holiday.write({'second_approver_id': current_employee.id})
                        else:
                            holiday.write({'first_approver_id': current_employee.id})
                        if holiday.holiday_type == 'employee' and holiday.type == 'remove':
                            holiday._validate_leave_request()
                        elif holiday.holiday_type == 'category':
                            leaves = self.env['hr.holidays']
                            for employee in holiday.category_id.employee_ids:
                                values = holiday._prepare_create_by_category(employee)
                                leaves += self.with_context(mail_notify_force_send=False).create(values)
                            # TODO is it necessary to interleave the calls?
                            leaves.action_approve()
                            if leaves and leaves[0].double_validation:
                                leaves.action_validate()
                else:
                    raise UserError(_('Hanya HR Manager Yang Bisa Approve Ini.'))
            else:
                if holidays.approve2.id == holidays.env.uid or holidays.env.uid == 1:
                    current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                    for holiday in self:
                        # if holiday.state not in ['confirm', 'validate1']:
                        #	raise UserError(_('Leave request must be confirmed in order to approve it.'))
                        # if holiday.state == 'validate1' and not holiday.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                        #	raise UserError(_('Only an HR Manager can apply the second approval on leave requests.'))

                        holiday.write({'state': 'validate'})
                        if holiday.double_validation:
                            holiday.write({'second_approver_id': current_employee.id})
                        else:
                            holiday.write({'first_approver_id': current_employee.id})
                        if holiday.holiday_type == 'employee' and holiday.type == 'remove':
                            holiday._validate_leave_request()
                        elif holiday.holiday_type == 'category':
                            leaves = self.env['hr.holidays']
                            for employee in holiday.category_id.employee_ids:
                                values = holiday._prepare_create_by_category(employee)
                                leaves += self.with_context(mail_notify_force_send=False).create(values)
                            # TODO is it necessary to interleave the calls?
                            leaves.action_approve()
                            if leaves and leaves[0].double_validation:
                                leaves.action_validate()
                else:
                    raise UserError(_('Anda Tidak Memiliki Hak Akses INI.'))
            return True

    @api.multi
    def action_draft(self):
        if self.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
            for holiday in self:
                if not holiday.can_reset:
                    raise UserError(_('Only an HR Manager or the concerned employee can reset to draft.'))
                if holiday.state not in ['confirm', 'refuse']:
                    raise UserError(
                        _('Leave request state must be "Refused" or "To Approve" in order to reset to Draft.'))
                holiday.write({
                    'state': 'draft',
                    'first_approver_id': False,
                    'second_approver_id': False,
                })
                linked_requests = holiday.mapped('linked_request_ids')
                for linked_request in linked_requests:
                    linked_request.action_draft()
                linked_requests.unlink()
            return True
        else:
            raise UserError(_('Hanya HR Manager Yang Bisa Mengembalikan Ke Draft.'))

    @api.multi
    def action_refuse(self):
        for holidays in self:
            if holidays.type == 'add' or holidays.env.uid == 1:
                if holidays.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                    current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                    for holiday in self:
                        if holiday.state not in ['confirm', 'validate', 'validate1']:
                            raise UserError(_('Leave request must be confirmed or validated in order to refuse it.'))

                        if holiday.state == 'validate1':
                            holiday.write({'state': 'refuse', 'first_approver_id': current_employee.id})
                        else:
                            holiday.write({'state': 'refuse', 'second_approver_id': current_employee.id})
                        # Delete the meeting
                        if holiday.meeting_id:
                            holiday.meeting_id.unlink()
                        # If a category that created several holidays, cancel all related
                        holiday.linked_request_ids.action_refuse()
                    self._remove_resource_leave()
                    return True
                else:
                    raise UserError(_('Hanya HR Manager Yang Bisa Refuse Ini.'))
            else:
                if holidays.approve2.id == holidays.env.uid or holidays.approve1.id == holidays.env.uid or holidays.env.uid == 1 or not holidays:
                    current_employee = holidays.env['hr.employee'].search([('user_id', '=', holidays.env.uid)], limit=1)
                    for holiday in self:
                        if holiday.state not in ['confirm', 'validate', 'validate1']:
                            raise UserError(_('Leave request must be confirmed or validated in order to refuse it.'))

                        if holiday.state == 'validate1':
                            holiday.write({'state': 'refuse', 'first_approver_id': current_employee.id})
                        else:
                            holiday.write({'state': 'refuse', 'second_approver_id': current_employee.id})
                        # Delete the meeting
                        if holiday.meeting_id:
                            holiday.meeting_id.unlink()
                        # If a category that created several holidays, cancel all related
                        holiday.linked_request_ids.action_refuse()
                    self._remove_resource_leave()
                    return True
                else:
                    raise UserError(_('Anda Tidak Memiliki Hak Akses INI.'))
