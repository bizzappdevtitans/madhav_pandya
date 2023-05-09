{
    "name": "Connector Trello",
    "summary": "To connect the trello to project model",
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
        "views/trello_backend_view.xml",
        "views/project_project_view.xml",
        "views/project_task_type.xml",
        "views/project_task_view.xml",
        "views/project_menu_view.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "licence": "LGPL-3",
}
