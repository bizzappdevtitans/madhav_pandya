from odoo import fields, models


class TrelloAbstractModel(models.AbstractModel):
    _name = "trello.model"
    _description = "My Abstract Model"

    trello_backend_ids = fields.Many2one(comodel_name="trello.backend")
    external_id = fields.Char("External id")
