from odoo import fields, models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_description = fields.Many2one('student',"Invoice Description")
    # new_field = fields.Char("New field1")
    confirmed_field1=fields.Many2one('student',"field1")
    delivery_description= fields.Text("Delivery Description")
    projectt= fields.Char("Project")
    taskk= fields.Char("Task Description")
    purchase_description= fields.Char("Purchase Description")
    manufact=fields.Char("Manufacturing Info")



    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals["invoice_description"] = self.invoice_description
        return invoice_vals



    # def _get_purchase_orders(self):
    #     print("Final method")
    #     invoice_vals=super(SaleOrder,self)._get_purchase_orders()
    #     invoice_vals.update({"purchase_description": self.purchase_description})
    #     return invoice_vals





























class StockRuleInherit(models.Model):
    _inherit = 'stock.rule'



























