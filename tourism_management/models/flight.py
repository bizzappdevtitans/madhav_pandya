from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class Flight(models.Model):
    _name = "flight"
    _description = "Flight Information"

    flight = fields.Selection(
        [
            ("indigo", "Indigo"),
            ("gofirst", "Go- First"),
            ("spicejet", "Spicejet"),
            ("emirates", "Emirates"),
            ("airasia", ("Air Asia")),
        ],
        string="Flight Name",
        default="indigo",
    )
    date_in = fields.Datetime(string="Departure", required=True)
    date_out = fields.Datetime(string="Arrival", required=True)
    place_from = fields.Selection(
        [("amdavad", "Sardar Vallabh Bhai Patel International Airport")],string="Place From"
    )
    place_to = fields.Selection(
        [
            ("dubai", "Dubai International Airport"),
            ("maldives", "Velana International Airport, Maldives"),
            ("philipines", "Ninoy Aquino International Airport,Philipines "),
        ],string="Place To"
    )
    fare = fields.Char(string="Price")
    booked_by = fields.Many2one(comodel_name="res.partner", string="Booked By")

    @api.constrains("date_in")
    def constrains_valid_date(self):
        """This will raise error if we select past dates"""
        if self.date_in < fields.Datetime.today():
            raise ValidationError("You cannot select past date")
