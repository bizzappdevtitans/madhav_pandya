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

    def _prepare_invoice(self):
        """Returns the value from sale.order to invoice"""
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals["invoice_description_id"] = self.invoice_description_id
        return invoice_vals
