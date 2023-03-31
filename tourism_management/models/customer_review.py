from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class CustomerReview(models.Model):
    _name= 'customer_review'
    _description='Customer Review'


    name=fields.Char("Customer Name")
    tour_name= fields.Selection([('dubai', 'Dubai'), ('philipines', 'Philipines'), ('maldives', 'Maldives')],string="Tour Name")
    priority = fields.Selection(
        [
            ("0", "Normal"),
            ("1", "low"),
            ("2", "High"),
            ("3", "Very-High"),
            ("4", "High-level"),
            ("5", "Full-too-High"),
        ],
        string="Feedback",
    )
    description= fields.Text(string="Description")
    photos= fields.Image(string= "Some photos of tour")


