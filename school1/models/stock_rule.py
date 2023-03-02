from odoo import fields,models




class StockRule(models.Model):
    _inherit="stock.rule"
    purchase_description=fields.Char("Purchase")




    # def _prepare_purchase_order(self,company_id, origins, values):
    #     print("\n\nHar har nMahaddev")
    #     invoice_vals=super(StockRule,self)._prepare_purchase_order(company_id, origins, values)
    #     invoice_vals.update({"purchase_description": self.purchase_description})
    #     return invoice_vals
