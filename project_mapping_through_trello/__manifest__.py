{
    "name": "Project Creation through Trello",
    "summary": "Creation of Project through Trello",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "sequence": 1,
    "website": "https://github.com/OCA/purchase-workflow",
    "version": "14.0.1.0.0",
    "depends": [
        "project",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project_menu_view.xml",
        "views/project_model_view.xml",
        "wizard/create_project_wizard.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
