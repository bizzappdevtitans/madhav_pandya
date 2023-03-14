from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    purchase_description = fields.Char("Purchase Description")
