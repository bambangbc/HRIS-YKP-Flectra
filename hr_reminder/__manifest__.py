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

    "depends": [
        "base", 
        "hr"
    ], 
    "auto_install": False, 
    "images": [
        "static/description/banner.jpg"
    ], 
    "data": [
        "security/ir.model.access.csv", 
        "security/hr_reminder_security.xml", 
        "views/hr_reminder_view.xml", 
        "views/reminder_template.xml"
    ], 
    "category": "Extra Tools", 
    "name": "Open HRMS Reminders Todo", 
    "license": "AGPL-3", 
    "author": "Betapy, Cybrosys Techno Solutions", 
    "support": "incoming+betapy/support@incoming.gitlab.com", 
    "summary": "HR Reminder For OHRMS", 
    "application": False, 
    "version": "2.0.0", 
    "qweb": [
        "static/src/xml/reminder_topbar.xml"
    ], 
    "installable": True
} 