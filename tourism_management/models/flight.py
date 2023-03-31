from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class Flight(models.Model):
    _name= 'flight'
    _description='Flight Information'

    flight= fields.Selection([('indigo', 'Indigo'),('gofirst', 'Go- First'), ('spicejet', 'Spicejet'),
     ('emirates', 'Emirates'), ('airasia', ('Air Asia'))],string="Flight Name",default="indigo")
    date_in= fields.Date("Date In")
    date_out= fields.Date("Date Out")
    place_from= fields.Char("From")
    place_to= fields.Char("To")
    fare= fields.Char("Price")
    booked_by= fields.Many2one(comodel_name="res.partner", string="Booked By")
    tour_reservation= fields.Many2one(comodel_name="tour", string="Tour Id")

