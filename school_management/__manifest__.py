{
    "name": "School",
    "summary": "Manage students and teachers.",
    "author": "BizzAppDev",
    "license": "AGPL-3",
    "sequence": 1,
    "website": "https://github.com/PacktPublishing" "/Odoo-15-Development-Essentials",
    "version": "15.0.1.0.0",
    "depends": [
        "mail",
        "sale",
        "account",
        "project",
        "sale_project",
        "purchase",
        "stock",
        'mrp',
    ],
    "data": [
        "data/cron.xml",
        "data/mail_template.xml",
        "views/school_view.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "wizard/create_appointment_view.xml",
        "views/student.xml",
        "views/teacher.xml",
        "views/student_appointment.xml",
        "reports/student_report.xml",
        "views/contact_us.xml",
        "views/director.xml",
        "views/results.xml",
        "views/admission.xml",
        "views/toppers.xml",
        "views/alumni.xml",
        "views/registration.xml",
        "views/fees.xml",
        "views/canteen.xml",
        "views/home.xml",
        "views/sale_order.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "school_management/scss/style.scss",
        ]
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "licence": "LGPL-3",
}
