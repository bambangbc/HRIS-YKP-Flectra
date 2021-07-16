{
    "name": "Overtime",
    "version": "0.1",
    "category": "HR",
    "sequence": 20,
    "author": "Bambang Bagus Candra",
    "website": "",
    "license": "AGPL-3",
    "summary": "Form Lembur Dan Perhitungan Lembur",
    "description": """
    * Tambah master perhitungan lembur (overtime type)
    * Tambah menu form lembur (overtime form)
    * Onchange department otomatis list employee muncul sesuai dengan dept yang sama
   
    """,
    "depends": ["hr",
                "resource",
                "hr_attendance",
                "hr_ykp_employees"
                ],
    "data":[
        "views/hr_overtime_view.xml",
        "reports/printout.xml",
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],

}

