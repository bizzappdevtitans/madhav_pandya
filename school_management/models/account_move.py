from odoo import fields, models


class AccountMove(models.Model):
    # inherited the object and added the field
    _inherit = "account.move"

    invoice_description_id = fields.Many2one(
        comodel_name="student", string="Invoice Description"
    )

    saleee_id= fields.Many2one(comodel_name='sale.order')


    lum_sum=fields.Boolean(string="Lum Sum",readonly=True)
