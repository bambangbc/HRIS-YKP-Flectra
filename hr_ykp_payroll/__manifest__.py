{
    "name": "Payroll YKP",
    "version": "0.1",
    "category": "HR",
    "sequence": 20,
    "author": "Bambang Bagus Candra",
    "website": "",
    "license": "AGPL-3",
    "summary": "Form Perhitungan Gaji",
    "description": """
    * Tambah master perhitungan lembur Gaji
    * Tambah menu form lembur Gaji
    * Onchange department otomatis list employee muncul sesuai dengan dept yang sama
   
    """,
    "depends": [
                "hr_payroll",
                "resource",
                "hr_attendance",
                "hr_ykp_employees"
                ],
    "data":[
        'security/ir.model.access.csv',
        "wizard/hr_payroll_pph21_by_employee.xml",
        "views/hr_payroll_view.xml",
        "views/hr_attendance.xml",
        "data/data.xml",
        "reports/slip_gaji.xml",
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],

}

