from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class TourItenerary(models.Model):
    _name = "tour_itenerary"
    _description = "Tour whole Information"

    tour_id = fields.Many2one("tour", string="Customer Inquiry")
    contact_name_id = fields.Many2one("res.partner", string="Contact Name")
    email = fields.Char("Email", required=True)
    mobile = fields.Char("Contact No", required=True)

    reference_noo = fields.Char(
        string="Order Reference",
        required=True,
        readonly=True,
        default=lambda self: ("New"),
    )

    prefer_start_date = fields.Date("Prefer Start Date", required=True)
    prefer_end_date = fields.Date("Prefer End date", required=True)
    room_required = fields.Selection([("one", "1"), ("two", "2"), ("three", "3")])
    adults = fields.Integer("Adults")
    children = fields.Integer("Children")
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")
    tour_days = fields.Char(string="Tour Days")

    tour_description_ids = fields.Many2many(
        comodel_name="tour_description", string="Tour Description"
    )

    _sql_constraints = [
        ("name_uniq", "UNIQUE (email)", "You cannot have same email!"),
    ]

    @api.constrains("prefer_start_date")
    def constrains_valid_date(self):
        """This will raise error if we select past dates"""
        if self.prefer_start_date < fields.Date.today():
            raise ValidationError("You cannot select past date")

    @api.onchange("prefer_end_date")
    def onchange_tour_days(self):
        """This counts the days of tours according to the start and end date"""
        for res in self:
            if res.prefer_start_date:
                res.tour_days = res.prefer_end_date - res.prefer_start_date

    @api.model
    def create(self, vals):
        """Returns the unique sequence number whenever new form is created"""
        if vals.get("reference_noo", ("New")) == ("New"):
            vals["reference_noo"] = self.env["ir.sequence"].next_by_code(
                "tour_itenerary"
            ) or _("New")
        res = super(TourItenerary, self).create(vals)
        return res

    def action_open_tour_description(self):
        """this will redirect to the records after clicking the smart button"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Tour Description",
            "view_mode": "tree,form",
            "res_model": "tour_description",
            "domain": [("id", "in", self.tour_description_ids.ids)],
            "context": "{'create': 'false'}",
        }

    @api.constrains("prefer_end_date", "prefer_start_date")
    def date_constrains(self):
        """This raise error if prefer start date is greater than prefer end state"""
        for rec in self:
            if rec.prefer_end_date < rec.prefer_start_date:
                raise ValidationError(
                    "Sorry, Prefer end date Must be greater Than prefer start date..."
                )

    def action_share_whatsapp_message(self):
        """This will send the message to travellers whatsapp by clicking send whatsapp button"""
        if not self.mobile:
            raise ValidationError("Traveller have not added their phone number")
        message = "Hi, Happy Journey"
        whatsapp_api_url = (
            "https://web.whatsapp.com/send?phone=",
            self.mobile,
            "&text=",
            message,
        )
        return {"type": "ir.actions.act_url", "target": "url", "url": whatsapp_api_url}

    def name_get(self):
        """Returns the reference number in Many2one field"""
        result = []
        for rec in self:
            name = rec.reference_noo
            result.append((rec.id, "%s" % (rec.reference_noo)))
        return result

    @api.constrains("mobile")
    def _check_phone_number(self):
        for rec in self:

            if rec.mobile == None:
                pass

            if len(rec.mobile) != 10 or rec.mobile.isdigit() == False:
                raise ValidationError("Insert your phone number properly")
