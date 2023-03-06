from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    field1 = fields.Many2one("student", "yoo")
