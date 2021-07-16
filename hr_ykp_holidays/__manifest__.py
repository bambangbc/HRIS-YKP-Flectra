{
    "name": "Holdays",
    "version": "0.1",
    "category": "HR",
    "sequence": 20,
    "author": "Bambang Bagus Candra",
    "website": "",
    "license": "AGPL-3",
    "summary": "Holidays",
    "description": """
    Holdays
   
    """,
    "depends": ["hr_holidays","hr_ykp_employees"
                ],
    "data":[
        "views/hr_holiday_view.xml",
        "views/hr_perdin_view.xml",
        "data/data.xml",
        "reports/printout.xml",
        "security/ir.model.access.csv",
        "security/ir_rule.xml"
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],

}

