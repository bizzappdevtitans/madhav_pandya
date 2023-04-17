from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_description_id = fields.Many2one(
        comodel_name="student", string="Invoice Description"
    )
    delivery_description = fields.Text("Delivery Description")
    project = fields.Char("Project")
    task = fields.Char("Task Description")
    purchase_description = fields.Char("Purchase Description")
    manufacture = fields.Char("Manufacturing Info")
    lum_sum= fields.Boolean(string="Lum Sum")


    # delivery_number= fields.Integer("Delivery Count", compute='_count_delivery')



    # @api.depends('picking_ids')
    # def _count_delivery(self):
    #     for order in self:
    #         order.delivery_count = len(order.picking_ids)



    def _prepare_invoice(self):
        print("\n\nInvoice Description")
        """Returns the value from sale.order to invoice"""
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({'invoice_description_id': self.invoice_description_id,
                            'lum_sum': self.lum_sum
            })
        return invoice_vals

    # def _prepare_invoice(self):
    #     print("\n\nLum Sum")
    #     """Returns the value from sale.order to invoice"""
    #     lum_sum_vals = super(SaleOrder, self)._prepare_invoice()
    #     lum_sum_vals["lum_sum"] = self.lum_sum
    #     return lum_sum_vals




    def _action_confirm(self):
        #self.order_line._action_launch_stock_rule()
        return super(SaleOrder, self)._action_confirm


    def create_delivery(self):
        delivery = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'origin': self.name,
            'sale_id': self.id,
            'location_id': self.partner_id.property_stock_customer.id,
            'location_dest_id': self.company_id.partner_id.property_stock_customer.id,
        })
        for line in self.order_line:
            self.env['stock.move'].create({
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'picking_id': delivery.id,
                'location_id': line.order_id.partner_id.property_stock_customer.id,
                'location_dest_id': self.company_id.partner_id.property_stock_customer.id,
            })
        return {
        'name': delivery.name,
        'type': 'ir.actions.act_window',
        'res_model': 'stock.picking',
        'view_mode': 'form',
        'res_id': delivery.id,
        'context': self.env.context,
        }


        @api.depends('delivery_order_ids')
        def compute_delivery_count(self):
            for record in self:
                record.delivery_count = len(record.delivery_order_ids)



        # def action_confirm(self):
        #     self.write({'state': 'sale'})
        #     return True

    # def create_delivery(self):
    #     delivery = self.env['stock.picking'].create({
    #         'partner_id': self.partner_id.id,
    #         'picking_type_id': self.env.ref('stock.picking_type_out').id,
    #         'origin': self.name,
    #         })
    #     return {
    #     'name': delivery.name,
    #     'type': 'ir.actions.act_window',
    #     'res_model': 'stock.picking',
    #     'view_mode': 'form',
    #     'res_id': delivery.id,
    #     'context': self.env.context,
    #     }
