from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    create_invoice = fields.Boolean("Create Invoice")
