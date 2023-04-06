from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class TourDescription(models.Model):
    _name = "tour.description"
    _description = "Tour Description"

    tour_code = fields.Integer(string="Tour Code")
    tour_days = fields.Char(string="Tour Days")
    tour_nights = fields.Integer(string="Tour Nights")
    tour_day_description = fields.Text(string="Tour Days Description")
    breakfast = fields.Boolean(string="Breakfast")
    lunch = fields.Boolean(string="Lunch")
    dinner = fields.Boolean(string="Dinner")
    products_id=fields.Many2one("product.product", string="Products")
