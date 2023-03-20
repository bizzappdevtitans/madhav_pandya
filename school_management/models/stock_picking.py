from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_description = fields.Text("Delivery Description")
    weight_measure=fields.Float("Weight measure")


    def _action_done(self):
        vals = super(StockPicking, self)._action_done()
        vals["weight_measure"] = self.weight_measure
        return vals
