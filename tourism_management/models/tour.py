from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class Tour(models.Model):
    _name = "tour"
    _description = "Tour Information"
    _rec_name = "tour_name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    tour_name = fields.Selection(
        [("dubai", "Dubai"), ("philipines", "Philipines"), ("maldives", "Maldives")],
        string="Tour Name",
        Tracking=True,
    )
    tour_name_id = fields.Many2one(comodel_name="package_info", string="country")

    tour_info_ids = fields.One2many(comodel_name="package_info", inverse_name="tour_id")

    tour_packages_id = fields.Many2one(
        related="tour_name_id.country", string="Click for Packages"
    )

    tour_type = fields.Selection(
        [
            ("type1", "Sightseeing Tours"),
            ("type2", "Shore Excursion Tours"),
            ("type3", "Adventure or Sporting Tours."),
        ],
        string="Tour type",
        Tracking=True,
    )

    information_line_ids = fields.Many2many(comodel_name="information_line")

    reference_no = fields.Char(
        string="Order Reference",
        required=True,
        readonly=True,
        default=lambda self: ("New"),
    )

    tour_details_ids = fields.Many2many(comodel_name="tour_details")

    information_count = fields.Integer(
        string="Information Count", compute="compute_count"
    )

    message_follower_id = fields.Char("Enter the message here")

    @api.depends("tour_details_ids")
    def compute_count(self):
        """this counts tour details and will show numbers on smart buttons"""
        for record in self:
            record.information_count = record.env["tour"].search_count(
                [("id", "in", self.tour_details_ids.ids)]
            )

    @api.model
    def create(self, vals):
        """Returns the unique sequence number whenever new form is created"""
        if vals.get("reference_no", ("New")) == ("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code("tour") or _(
                "New"
            )
        res = super(Tour, self).create(vals)
        return res

    def name_get(self):
        """Returns the reference number in Many2one field"""
        result = []
        for rec in self:
            name = rec.reference_no
            result.append((rec.id, "%s" % (rec.reference_no)))
        return result

    def action_open_tour_details(self):
        """this will redirect to the records after clicking the smart button"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Tour",
            "view_mode": "tree",
            "res_model": "tour_details",
            "domain": [("id", "in", self.tour_details_ids.ids)],
            "context": "{'create': 'false'}",
        }

    def action_open_flight_details(self):
        """this will redirect to the records after clicking the smart button"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Flight",
            "view_mode": "tree",
            "res_model": "information_line",
            "domain": [("id", "in", self.information_line_ids.ids)],
            "context": "{'create': 'false'}",
        }

    def default_get(self, fields):
        """Returns the default value when someone try to create the new form"""
        res = super(Tour, self).default_get(fields)
        res["tour_name"] = "dubai"
        res["tour_type"] = "type1"
        return res
