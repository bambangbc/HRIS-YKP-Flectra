# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
###################################################################################
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Copyright (C) 2018 BetaPy
#    Authors: BetaPy, Avinash Nk, Jesni Banu (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

{
    "category": "Generic Modules/Human Resources", 
    "website": "https://betapy.com", 
    "name": "Open HRMS Core", 
    "license": "AGPL-3", 
    "author": "Betapy, Cybrosys Techno Solutions", 
    "demo": [], 

    "summary": "Open HRMS Suit: It brings all Open HRMS modules", 
    "application": True, 
    "depends": [
        "hr_payroll_account", 
        "hr_gamification",
        "hr_employee_updation", 
        "hr_recruitment", 
        "hr_attendance", 
        "hr_holidays", 
        "hr_payroll", 
        "hr_expense", 
        "hr_leave_request_aliasing", 
        "hr_timesheet", 
        "oh_appraisal", 
        "oh_employee_creation_from_user", 
        "oh_employee_documents_expiry", 
        "hr_multi_company", 
        "ohrms_loan_accounting", 
        "ohrms_salary_advance", 
        "hr_reminder", 
        "hr_reward_warning", 
        "hr_theme"
    ], 
    "version": "2.0.0", 
    "auto_install": False, 
    "images": [
        "static/description/banner.jpg"
    ], 
    "data": [
        "views/menu_arrangement_view.xml", 
        "views/hr_config_view.xml"
    ], 
    "support": "incoming+betapy/support@incoming.gitlab.com", 
    "installable": True, 
    "description": "Main module of Open HRMS. It brings all others into a single module"
} 