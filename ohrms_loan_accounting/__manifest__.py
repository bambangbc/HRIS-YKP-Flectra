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
    "category": "Human Resources", 
    "website": "https://betapy.com", 

    "name": "Open HRMS Loan Accounting", 
    "license": "AGPL-3", 
    "author": "Betapy, Cybrosys Techno Solutions", 
    "demo": [], 

    "summary": "Open HRMS Loan Accounting", 
    "application": False, 
    "depends": [
        "base", 
        "hr_payroll", 
        "hr", 
        "account", 
        "ohrms_loan"
    ], 
    "version": "2.0.0", 
    "auto_install": False, 
    "images": [
        "static/description/banner.jpg"
    ], 
    "data": [
        "views/hr_loan_config.xml", 
        "views/hr_loan_acc.xml"
    ], 
    "support": "incoming+betapy/support@incoming.gitlab.com", 
    "installable": True, 
    "description": "\n        Create accounting entries for loan requests.\n        "
} 