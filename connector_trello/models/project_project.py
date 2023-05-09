from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    trello_bind_ids = fields.One2many(
        comodel_name="trello.project.project", inverse_name="odoo_id", readonly=True
    )
    external_id = fields.Char("External Id", related="trello_bind_ids.external_id")
    api_key = fields.Char("Api key")
    token = fields.Char("Token Key")
