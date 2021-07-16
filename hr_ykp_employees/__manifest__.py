# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Directory',
    'author' : 'Odoo S.A',
    'version': '1.1',
    'category': 'Human Resources',
    'sequence': 75,
    'summary': 'Jobs, Departments, Employees Details',
    'description': "",
    'website': 'https://flectrahq.com/page/employees',
    'images': [
        #'images/hr_department.jpeg',
        #'images/hr_employee.jpeg',
        #'images/hr_job_position.jpeg',
        #'static/src/img/default_image.png',
    ],
    'depends': [
        'base_setup',
        'mail',
        'resource',
        'web',
        'hr',
        'hr_contract',
        'hr_ykp_training',
        'hr_ykp_appraisal'
    ],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        #'views/hr_views.xml',
        #'views/hr_templates.xml',
        'views/hr_employee.xml',
        'reports/cv.xml',
        #'data/hr_data.xml',
    ],
    'demo': [
        #'data/hr_demo.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
