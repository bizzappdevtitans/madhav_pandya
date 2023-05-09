from odoo import fields, models


class TrelloProjectTaskType(models.Model):
    _name = "trello.project.task.type"
    _description = "Trello Project Task Type"
    _inherits = {"project.task.type": "odoo_id"}
    _inherit = ["trello.model"]

    odoo_id = fields.Many2one(
        comodel_name="project.task.type", required=True, ondelete="cascade"
    )
