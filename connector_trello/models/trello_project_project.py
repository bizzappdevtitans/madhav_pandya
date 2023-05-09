from odoo import fields, models


class TrelloProject(models.Model):
    _name = "trello.project.project"
    _description = "Trello Project Project"
    _inherits = {"project.project": "odoo_id"}
    _inherit = ["trello.model"]

    external_id = fields.Char("external_id")

    odoo_id = fields.Many2one(
        comodel_name="project.project", required=True, ondelete="cascade"
    )
