from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit="product.template"


    weight_done= fields.Boolean(string="Weight Done")
    # grid_product_tmpl_id= fields.Many2one("product.template",related="order_line.grid_product_tmpl_id")
    sale_history= fields.One2many(comodel_name="sale.order",inverse_name="grid_product_tmpl_id")


    price_list_ids= fields.Many2many(comodel_name='extra.price.list',string="Extra Price List")


    total_price= fields.Float("Total Price",compute="_compute_total_amount")

    calculated_amount= fields.Float(string="Calculated amount",compute="compute_total_calculated_amount")



    @api.depends('calculated_amount')
    def compute_total_calculated_amount(self):
        for rec in self:
            rec.update({'calculated_amount': rec.total_price*rec.standard_price})


    def _compute_total_amount(self):
        for record in self:
            record.total_price=sum(record.price_list_ids.mapped('price'))



