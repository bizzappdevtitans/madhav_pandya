from odoo import fields, models


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    trello_bind_ids = fields.One2many(
        comodel_name="trello.project.task.type", inverse_name="odoo_id", readonly=True
    )
    external_id = fields.Char(
        string="external_id", related="trello_bind_ids.external_id"
    )
    api_key = fields.Char("Api key")
    token = fields.Char("Token")
    project_external_id = fields.Char(
        string="Project External Id", related="trello_bind_ids.project_external_id"
    )
