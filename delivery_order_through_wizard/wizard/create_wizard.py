from odoo import _, fields, models
from odoo.exceptions import ValidationError


class CreateDeliveryWizard(models.TransientModel):
    _name = "create.delivery.wizard"
    _description = "Create Wizard"

    unit = fields.Integer(default=1, uom="units")

    def get_delivery_order_payload(self):
        """Method returns the delivery order payload"""

        return {
            "name": "AT/PL:123056:",
            "customer": {
                "name": "xyz",
                "address": {
                    "city": "Pune",
                    "country": "",
                    "zip": "10ji033",
                    "phone": "9900266933",
                },
            },
            "source_location": {"name": "sourceee", "operation_type": "internal"},
            "stock_operation_type": {"name": "delivery order", "sequence_code": "OUT"},
            "destination_location": {
                "name": "destination",
                "operation_type": "internal",
            },
            "move_lines": [
                {"productId": "5112976146", "quantity": 3},
                {"productId": "5112974885", "quantity": 15},
                {"productId": "5112973994", "quantity": 3},
            ],
        }

    def create_delivery_order_mapping(self):
        """Method creates the delivery order through delivery_payload and fetch the
        products on the basis of barcode"""
        record = self.get_delivery_order_payload()

        move_values = []

        for values in record["move_lines"]:
            product = self.env["product.product"].search(
                [("barcode", "=", values.get("productId"))]
            )
            if not product:
                raise ValidationError(
                    _("Product with Barcode  %s not found" % values.get("productId"))
                )
            move_values.append(
                (
                    0,
                    0,
                    {
                        "product_id": product.id,
                        "product_uom_qty": values.get("quantity"),
                        "name": product.id,
                        "product_uom": self.unit,
                    },
                )
            )

        location_value = self.env["stock.location"].search(
            [("name", "=", record.get("source_location").get("name"))]
        )

        if not location_value:
            location_value = self.env["stock.location"].create(
                {
                    "name": record.get("source_location").get("name"),
                    "usage": record.get("source_location").get("operation_type"),
                }
            )
        destination_value = self.env["stock.picking.type"].search(
            [
                (
                    "sequence_code",
                    "=",
                    record.get("stock_operation_type").get("sequence_code"),
                )
            ]
        )
        location_destination = self.env["stock.location"].search(
            [("name", "=", record.get("destination_location").get("name"))]
        )

        if not location_destination:
            location_destination = self.env["stock.location"].create(
                {
                    "name": record.get("destination_location").get("name"),
                    "usage": record.get("destination_location").get("operation_type"),
                }
            )

        user = self.env["res.partner"].search(
            [("name", "=", record.get("customer").get("name"))]
        )

        if not user:
            partner_name = self.env["res.partner"].create(
                {
                    "name": record.get("customer").get("name"),
                    "city": record.get("customer").get("address").get("city"),
                    "zip": record.get("customer").get("address").get("zip"),
                    "phone": record.get("customer").get("address").get("phone"),
                }
            )
        else:
            partner_name = user
        delivery_value = self.env["stock.picking"].search(
            [("name", "=", record.get("name"))]
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
                    "name": record.get("name"),
                    "partner_id": partner_name.id,
                    "location_id": location_value.id,
                    "picking_type_id": destination_value.id,
                    "location_dest_id": location_destination.id,
                    "move_lines": move_values,
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
