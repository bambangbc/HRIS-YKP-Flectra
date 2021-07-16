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
    "website": "https://betapy.com", 

    "description": "Roll out appraisal plans and get the best of your workforce", 

    "depends": [
        "base", 
        "hr", 
        "survey"
    ], 
    "images": [
        "static/description/banner.jpg"
    ], 
    "data": [
        "security/ir.model.access.csv", 
        "security/hr_appraisal_security.xml", 
        "views/hr_appraisal_survey_views.xml", 
        "views/hr_appraisal_form_view.xml", 
        "data/hr_appraisal_stages.xml"
    ], 
    "category": "Human Resources", 
    "name": "Open HRMS Employee Appraisal", 
    "license": "AGPL-3", 
    "author": "Betapy, Cybrosys Techno Solutions", 
    "support": "incoming+betapy/support@incoming.gitlab.com", 
    "summary": "Roll out appraisal plans and get the best of your workforce", 
    "application": False, 
    "version": "2.0.0", 
    "installable": True
} 