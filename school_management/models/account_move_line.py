from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    field_id = fields.Many2one(comodel_name="student", string="Field value")
