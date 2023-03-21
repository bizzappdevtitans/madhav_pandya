from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_description = fields.Text("Delivery Description")
    weight_measure=fields.Float("Weight measure")


