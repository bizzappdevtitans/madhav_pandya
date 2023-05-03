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
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/create_delivery_order_wizard.xml",
        "views/delivery_order_menu.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
