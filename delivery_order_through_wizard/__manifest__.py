{
    "name": "Delivery Order Management",
    "summary": "Creation of Delivery Order through Wizard",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "sequence": 1,
    "website": "https://github.com/OCA/purchase-workflow",
    "version": "14.0.1.0.0",
    "depends": [
        "stock",
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/delivery_order_menu.xml",
        "wizard/create_wizard.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "licence": "LGPL-3",
}
