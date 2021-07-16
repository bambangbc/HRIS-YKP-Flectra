# -*- coding: utf-8 -*-
{
    'name': "hr_ykp_training",

    'summary': """
        Module YKP HR Training""",

    'description': """
        Module YKP HR Training
    """,

    'author': "GNI",
    'website': "http://www.gni.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'hr',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'data/sequence.xml',
        # 'data/records.xml',
        'security/hr_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        "reports/printout.xml",
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}