from odoo import fields, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        inv_obj = super(SaleAdvancePaymentInv, self)._create_invoice(
            order, so_line, amount
        )
        inv_obj.update({'invoice_description_id': order.invoice_description_id,
                            'lum_sum': order.lum_sum
            })
        return inv_obj
