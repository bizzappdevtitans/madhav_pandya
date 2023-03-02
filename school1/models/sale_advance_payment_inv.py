from odoo import fields, models



class SaleAdvancePaymentInv(models.TransientModel):
    _inherit="sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        inv_obj = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        inv_obj["invoice_description"]= order.invoice_description
        return inv_obj
