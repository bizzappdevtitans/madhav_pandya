from odoo import fields, models


class director(models.Model):
    _name = "director"
    _description = "Director"

    name = fields.Char(string="Name")
    LastName = fields.Char(string="Last Name")
    ContactNo = fields.Char("ContactNO")
    email = fields.Char("email")
    experience = fields.Char("experience")
    department = fields.Char("Department")
    image = fields.Image("Photo")
    aadhar = fields.Image("Aadhar")

    _sql_constraints = [
        ("department_uniq", "UNIQUE(department)", "You cannot repeat same Department")
    ]
