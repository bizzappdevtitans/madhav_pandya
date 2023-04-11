from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_description_id = fields.Many2one(
        comodel_name="student", string="Invoice Description"
    )
    delivery_description = fields.Text("Delivery Description")
    project = fields.Char("Project")
    task = fields.Char("Task Description")
    purchase_description = fields.Char("Purchase Description")
    manufacture = fields.Char("Manufacturing Info")
    lum_sum= fields.Boolean(string="Lum Sum")

    def _prepare_invoice(self):
        print("\n\nInvoice Description")
        """Returns the value from sale.order to invoice"""
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({'invoice_description_id': self.invoice_description_id,
                            'lum_sum': self.lum_sum
            })
        return invoice_vals

    # def _prepare_invoice(self):
    #     print("\n\nLum Sum")
    #     """Returns the value from sale.order to invoice"""
    #     lum_sum_vals = super(SaleOrder, self)._prepare_invoice()
    #     lum_sum_vals["lum_sum"] = self.lum_sum
    #     return lum_sum_vals
