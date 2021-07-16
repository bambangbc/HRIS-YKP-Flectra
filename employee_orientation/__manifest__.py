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
    "description": "Complete Employee Orientation/Training Program",
    "license": "AGPL-3",
    "website": "https://betapy.com",
    "auto_install": False,
    "category": "Generic Modules/Human Resources",
    "version": "2.0.0",
    "support": "incoming+betapy/support@incoming.gitlab.com",
    "company": "Cybrosys Techno Solutions",
    "depends": [
        "base",
        "hr"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/orientation_complete.xml",
        "views/orientation_checklist_line.xml",
        "views/orientation_checklist.xml",
        "views/employee_orientation.xml",
        "views/orientation_checklists_request.xml",
        "views/orientation_checklist_sequence.xml",
        "views/orientation_request_mail_template.xml",
        "views/employee_training.xml"
    ],
    "name": "Employee Orientation & Training",
    "application": False,
    "images": [
        "static/description/banner.jpg"
    ],
    "installable": True,
    "summary": "Employee Orientation/Training Program",
    "author": "Betapy, Cybrosys Techno Solutions"
} 