from odoo import fields, api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    field_id = fields.Many2one(comodel_name="student", string="New field")
    delivery_description = fields.Text("Delivery Description")
    manufacture = fields.Char("manufacture")
    weight_measure = fields.Float("Weight measure")

    def _get_new_picking_values(self):
        """Returns the value from sale.order to stock.picking model"""
        vals = super(StockMove, self)._get_new_picking_values()
        vals["delivery_description"] = self.sale_line_id.order_id.delivery_description
        return vals

    def _prepare_procurement_values(self):
        """Returns the value from SO to MO"""
        res = super()._prepare_procurement_values()
        res["manufacture"] = self.sale_line_id.order_id.manufacture
        return res

    def _action_done(self, cancel_backorder=False):
        """Returns the value from stock.move to sale.order.line"""
        res = super(StockMove, self)._action_done(cancel_backorder)
        for rec in self:
            if not rec.sale_line_id or not rec.sale_line_id.product_id.weight_done:
                continue
            rec.sale_line_id.weight_measure = rec.weight_measure
            return res

    def _get_new_picking_values(self):
        """Returns the value from sale.order.line to stock.move"""
        vals = super(StockMove, self)._get_new_picking_values()
        for rec in self:
            rec.weight_measure = rec.sale_line_id.weight_measure
            return vals
