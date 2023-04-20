{
    "name": "Delivery Order Mapping ",
    "summary": "Creation of Delivery Order through Wizard",
    "author": "BizzAppDev",
    "license": "AGPL-3",
    "sequence": 1,
    "website": "",
    "version": "14.0.1.0.0",
    "depends": [
        "stock",
        'base',
    ],
    "data": [
        "wizard/create_wizard.xml",
        "views/delivery_order_menu.xml",
        "security/ir.model.access.csv",

    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "licence": "LGPL-3",
}
