from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    trello_bind_ids = fields.One2many(
        comodel_name="trello.project.task", inverse_name="odoo_id", readonly=True
    )
    external_id = fields.Char("External id", related="trello_bind_ids.external_id")
