# -*- coding: utf-8 -*-
{
    'name': "debranding",

    'summary': """
        Flectra Debranding""",

    'description': """
        Flectra Debranding
    """,

    'author': "Wavest",
    'website': "http://wavest.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'debranding',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/js.xml',
        'views/templates.xml',
    ],    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/web.xml',
    ],
}