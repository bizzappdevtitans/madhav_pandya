from odoo import fields, models


class school(models.Model):
    _name = "school"
    _description = "School Information"

    name = fields.Char(string="School Name")
    LastName = fields.Char(string="School type")
    ContactNo = fields.Char("ContactNO")
    Address = fields.Char("Address")
    image = fields.Image(string="image")
    booleaa = fields.Boolean(string="English Medium")
