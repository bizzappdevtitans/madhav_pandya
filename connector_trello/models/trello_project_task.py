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
    api_key = fields.Char("Api_key")
    token = fields.Char("Token")
    project_external_id = fields.Char("project_external_id")
    task_created_date = fields.Datetime("Task Created Date")
