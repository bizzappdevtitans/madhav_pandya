from odoo import fields, models


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    trello_bind_ids = fields.One2many(
        comodel_name="trello.project.task.type", inverse_name="odoo_id", readonly=True
    )
    external_id = fields.Char("external_id", related="trello_bind_ids.external_id")
