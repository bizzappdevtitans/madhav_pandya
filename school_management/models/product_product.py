from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit="product.product"


    purchase_history_ids= fields.One2many(comodel_name="purchase.order.line",inverse_name="product_id",limit=5)
    sale_history_ids=fields.One2many(comodel_name="sale.order.line", inverse_name="product_id",limit=5)
