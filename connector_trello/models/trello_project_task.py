from odoo import fields, models


class TrelloProjectTask(models.Model):
    _name = "trello.project.task"
    _description = "Trello Project Task"
    _inherits = {"project.task": "odoo_id"}
    _inherit = ["trello.model"]

    odoo_id = fields.Many2one(
        comodel_name="project.task", required=True, ondelete="cascade"
    )

    external_id = fields.Char("external_id")
