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
    "category": "Human Resource", 
    "website": "https://betapy.com", 

    "name": "Open HRMS Dashboard", 
    "license": "AGPL-3", 
    "author": "Betapy, Cybrosys Techno Solutions", 

    "support": "incoming+betapy/support@incoming.gitlab.com", 
    "summary": "Open HRMS Dashboard", 
    "application": True, 
    "depends": [
        "hr", 
        "hr_holidays", 
        "hr_timesheet", 
        "hr_payroll", 
        "hr_attendance", 
        "hr_timesheet_attendance", 
        "hr_recruitment"
    ], 
    "version": "2.0.0", 
    "images": [
        "static/description/banner.jpg"
    ], 
    "data": [
        "views/dashboard_views.xml"
    ], 
    "qweb": [
        "static/src/xml/hrms_dashboard.xml"
    ], 
    "installable": True, 
    "description": "Open HRMS Dashboard"
} 