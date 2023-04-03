from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class InformationLine(models.Model):
    _name = "information_line"
    _description = "Tour Information"

    start_place = fields.Char(string="From", default="Ahmedabad", readonly=True)
    end_place = fields.Selection(
        [("dubai", "Dubai"), ("philipines", "Philipines"), ("maldives", "Maldives")], string="To"
    )
    transport_type = fields.Selection(
        [("bus", "Bus"), ("train", "Train"), ("flight", "Flight")],required=True,string="Transport type"
    )
    travel_class = fields.Selection([("c1", "First Class"), ("c2", "Second class")], required=True,string="Travel class")
    distance = fields.Char(string="Distance",required=True)
    fare = fields.Float(string="Fare",required=True)
