from odoo import fields,models


class StockMove(models.Model):
    _inherit = "stock.move"

    field1 = fields.Text("New field")
    delivery_description = fields.Text('Delivery Description')


    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        print("Madhav.............")
        vals['delivery_description'] = self.sale_line_id.order_id.delivery_description
        return vals

