from odoo import fields, models
from odoo.exceptions import ValidationError, UserError


class CreateWizard(models.TransientModel):
    _name = "create.wizard"
    _description = "Create Wizard"

    unit = fields.Integer(default=1, uom="units")

    def get_payload(self):
        """Method returns the delivery order payload"""

        return {
            "name": "AT/PL:123456:",
            "customer": {
                "name": "xyz",
                "address": {
                    "city": "Pune",
                    "country": "",
                    "zip": "10ji033",
                    "phone": "9900266933",
                },
            },
            "move_lines": [
                {"productId": "5112976146", "quantity": 3},
                {"productId": "5112974885", "quantity": 15},
                {"productId": "5112973994", "quantity": 3},
            ],
        }

    def create_delivery_order_mapping(self):
        """Method creates the delivery order on the basis of partner value and fetch and
        fetch the products on the basis of barcode"""
        record = self.get_payload()

        name_value = record["name"]
        partner_value = record["customer"]["name"]
        city = record["customer"]["address"]["city"]
        zipp = record["customer"]["address"]["zip"]
        phone = record["customer"]["address"]["phone"]
        barcode = record["move_lines"][0]["productId"]
        barcode_two = record["move_lines"][1]["productId"]
        barcode_three = record["move_lines"][2]["productId"]
        quantity = record["move_lines"][0]["quantity"]
        quantity_one = record["move_lines"][1]["quantity"]
        quantity_two = record["move_lines"][2]["quantity"]

        product_one = self.env["product.product"].search([("barcode", "=", barcode)])

        if not product_one:
            raise ValidationError("Sorry the barcode didn't match with any of product")
        product_two = self.env["product.product"].search(
            [("barcode", "=", barcode_two)]
        )
        if not product_two:
            raise ValidationError("Sorry the barcode didn't match with any of product")

        product_three = self.env["product.product"].search(
            [("barcode", "=", barcode_three)]
        )
        if not product_three:
            raise ValidationError("Sorry the barcode didn't match with any of product")

        location_value = self.env["stock.location"].search([("name", "=", "Stock")])
        destination_value = self.env["stock.picking.type"].search(
            [("sequence_code", "=", "OUT")]
        )
        location_value_2 = self.env["stock.location"].search(
            [("name", "=", "Customers")]
        )

        user = self.env["res.partner"].search([("name", "=", "xyz")])

        if not user.id:
            partner_name = self.env["res.partner"].create(
                {"name": partner_value, "city": city, "zip": zipp, "phone": phone}
            )
        else:
            partner_name = self.env["res.partner"].search([("name", "=", "xyz")])

        delivery_value = self.env["stock.picking"].search(
            [("name", "=", "AT/PL:123456:")]
        )
        if delivery_value:
            return {
                "name": delivery_value.name,
                "type": "ir.actions.act_window",
                "res_model": "stock.picking",
                "view_mode": "form",
                "res_id": delivery_value.id,
                "context": self.env.context,
            }
        else:
            partner_values = self.env["stock.picking"].create(
                {
                    "name": name_value,
                    "partner_id": partner_name.id,
                    "location_id": location_value.id,
                    "picking_type_id": destination_value.id,
                    "location_dest_id": location_value_2.id,
                    "move_lines": [
                        (
                            0,
                            0,
                            {
                                "product_id": product_one.id,
                                "product_uom_qty": quantity,
                                "name": product_one.id,
                                "product_uom": self.unit,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "product_id": product_two.id,
                                "product_uom_qty": quantity_one,
                                "name": product_two.id,
                                "location_id": location_value.id,
                                "product_uom": self.unit,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "product_id": product_three.id,
                                "product_uom_qty": quantity_two,
                                "name": product_three.id,
                                "location_id": location_value.id,
                                "product_uom": self.unit,
                            },
                        ),
                    ],
                }
            )

            return {
                "name": partner_values.name,
                "type": "ir.actions.act_window",
                "res_model": "stock.picking",
                "view_mode": "form",
                "res_id": partner_values.id,
                "context": self.env.context,
            }
