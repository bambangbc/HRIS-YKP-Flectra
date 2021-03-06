# -*- coding: utf-8 -*-
{
    'name': "hr_ykp_recruitment",

    'summary': """
        YKP Recruitment Survey""",

    'description': """
        Long description of module's purpose
    """,

    'author': "GNI",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['survey', 'hr_recruitment', 'website_hr_recruitment'],

    # always loaded
    'data': [
        'data/config.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}