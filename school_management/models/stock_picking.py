from odoo import fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    delivery_description = fields.Text("Delivery Description")
    weight_measure = fields.Float("Weight measure")

    def button_validate(self):
        for rec in self:
            if rec.picking_type_id.create_invoice == True:
                print("\n\nMAdhav Pandya")
                vals = self.env["sale.advance.payment.inv"].search([])
                for rec in vals:
                    rec.create_invoices()

            else:
                print("Pandyaaaaaaaaaaaaaaaa")
