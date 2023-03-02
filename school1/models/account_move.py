from odoo import fields,models



class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_description = fields.Many2one("student","Invoice Description")
