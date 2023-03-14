from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_description = fields.Text("Delivery Description")
