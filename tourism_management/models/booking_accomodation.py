from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class BookingAccomodation(models.Model):
    _name = "booking.accomodation"
    _description = "Booking Information"

    tour_name = fields.Selection(
        [("dubai", "Dubai"), ("philipines", "Philipines"), ("maldives", "Maldives")],
        string="Tour Name",help="Tour Name"
    )
    hotel_dubai = fields.Selection(
        [
            ("hotel1", "Hotel Burj Al Arab"),
            ("hotel2", "Hotel Atlantis The Palm"),
            ("hotel3", "Hotel Atlantis The Palm"),
        ],
        string="Hotel Dubai", help="Hotel Dubai"
    )
    hotel_philipines = fields.Selection(
        [
            ("hotel1", "Hotel Hennan Resort Alona Beach"),
            ("hotel2", "Hotel Prime Asia"),
            ("hotel3", "Hotel Diamond"),
        ],string="Hotel Philipines", help="Hotel Philipines"
    )
    hotel_maldives = fields.Selection(
        [
            ("hotel1", '"The St. Regis Maldives Vommuli Resort"'),
            ("hotel2", '"Cheval Blanc Randheli"'),
            ("hotel3", '"Velaa Private Island"'),
            ("hotel4", "Radisson Blu Resort Maldives"),
        ],string="Hotel Maldives", help="Hotel Philipines"
    )

    date_in = fields.Date(string="Check in", required=True)
    date_out = fields.Date(string="Check out", required=True)

    room_type = fields.Selection(
        [
            ("duplex", "Duplex room"),
            ("delux", "Delux Room"),
            ("delux_jac", "Delux Room with jackuzi"),
        ],
        required=True,string="Room Type"
    )
    days = fields.Char(string="Days")
    meal = fields.Selection(
        [("veg", "Veg"), ("non_veg", "NOn-Veg"), ("jain", "Jain")], required=True,string="Meal"
    )

    cost_per_night = fields.Integer(sting="Cost per night")

    total_cost = fields.Text(string="Total cost")

    @api.onchange("date_out")
    def onchange_hotel_days(self):
        """This counts the days of staying at hotel according to the check in and check out"""
        for res in self:
            if res.date_in:
                res.days = res.date_out - res.date_in

    @api.onchange("hotel_dubai")
    def _onchange_cost(self):
        """This update the cost per night according to the selected hotels of dubai"""
        for rec in self:
            if rec.hotel_dubai == "hotel1":
                rec.update({"cost_per_night": 100000})
            elif rec.hotel_dubai == "hotel2":
                rec.update({"cost_per_night": 200000})
            elif rec.hotel_dubai == "hotel3":
                rec.update({"cost_per_night": 3000000})

    @api.onchange("hotel_philipines")
    def _onchange_cost1(self):
        """This update the cost per night according to the selected hotel of philipines"""
        for rec in self:
            if rec.hotel_philipines == "hotel1":
                rec.update({"cost_per_night": 111000})
            elif rec.hotel_philipines == "hotel2":
                rec.update({"cost_per_night": 210000})
            elif rec.hotel_philipines == "hotel3":
                rec.update({"cost_per_night": 3040000})

    @api.onchange("hotel_maldives")
    def _onchange_cost2(self):
        """This update the cost per night according to the selected hotel of maldives"""
        for rec in self:
            if rec.hotel_maldives == "hotel1":
                rec.update({"cost_per_night": 1156000})
            elif rec.hotel_maldives == "hotel2":
                rec.update({"cost_per_night": 215600})
            elif rec.hotel_maldives == "hotel3":
                rec.update({"cost_per_night": 3040000})

    @api.constrains("date_out", "date_in")
    def date_constrains(self):
        """This checks that date out must be greater than date in"""
        for rec in self:
            if rec.date_out < rec.date_in:
                raise ValidationError("Sorry, date out Must be greater Than date in...")

    def action_sure_confirm(self):
        """This raise the pop up when user have selected the hotel and than click confirm button"""
        if self.tour_name:
            return {
                "effect": {
                    "fadeout": "slow",
                    "message": "Your Hotel Booking is confirmed",
                    "type": "rainbow_man",
                }
            }

    @api.constrains("date_in")
    def constrains_valid_date(self):
        """This will raise error if we select past dates"""
        for rec in self:
            if self.date_in < fields.Date.today():
                raise ValidationError("You cannot select past date")
