from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit="product.template"


    weight_done= fields.Boolean(string="Weight Done")
    # grid_product_tmpl_id= fields.Many2one("product.template",related="order_line.grid_product_tmpl_id")
    sale_history= fields.One2many(comodel_name="sale.order",inverse_name="grid_product_tmpl_id")
