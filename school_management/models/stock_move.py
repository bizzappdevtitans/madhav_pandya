from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    field_id = fields.Many2one(comodel_name="student", string="New field")
    delivery_description = fields.Text("Delivery Description")
    manufacture = fields.Char("manufacture")

    def _get_new_picking_values(self):
        """Returns the value from sale.order to stock.move model"""
        vals = super(StockMove, self)._get_new_picking_values()
        vals["delivery_description"] = self.sale_line_id.order_id.delivery_description
        return vals

    def _prepare_procurement_values(self):
        """Returns the value from SO to MO"""
        res = super()._prepare_procurement_values()
        res["manufacture"] = self.sale_line_id.order_id.manufacture
        return res
