from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit="product.template"


    weight_done= fields.Boolean(string="Weight Done")
