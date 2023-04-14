from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit="product.template"


    weight_done= fields.Boolean(string="Weight Done")
    # grid_product_tmpl_id= fields.Many2one("product.template",related="order_line.grid_product_tmpl_id")
    sale_history= fields.One2many(comodel_name="sale.order",inverse_name="grid_product_tmpl_id")


    extra_price_of_product= fields.Float(string="Price")

    price_list=fields.Many2one(comodel_name='extra.price.list',string='Price list')

    price_list_ids= fields.Many2many(comodel_name='extra.price.list',limit=1)


    total_price= fields.Float("Total Price",compute="compute_total_price")



    @api.depends('total_price')
    def compute_total_price(self):
        for rec in self:
            rec.update({'total_price': rec.extra_price_of_product*rec.standard_price})
