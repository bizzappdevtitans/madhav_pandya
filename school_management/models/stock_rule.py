from odoo import fields, models


class StockRule(models.Model):
    _inherit = "stock.rule"
    purchase_description = fields.Char("Purchase")

    def _prepare_mo_vals(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
        bom,
    ):
        """Returns the values from SO to MO"""

        res = super()._prepare_mo_vals(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
        )
        res["manufacture"] = values.get("manufacture")
        return res
