from odoo import fields, models


class MrpWorkOrder(models.Model):
    _inherit="mrp.workorder"
    manufact= fields.Char("Manufacturing")




    def _action_confirm(self):
        print("Final method1")
        invoice_vals=super(MrpWorkOrder,self)._action_confirm()
        invoice_vals["manufact"]= self.manufac
        return invoice_vals
