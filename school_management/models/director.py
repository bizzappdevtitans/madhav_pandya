from odoo import fields, models


class Director(models.Model):
    _name = "director"
    _description = "Director"

    name = fields.Char(string="Name")
    lastname = fields.Char(string="Last Name")
    contact_no = fields.Char("contact_no")
    email = fields.Char("email")
    experience = fields.Char("experience")
    department = fields.Char("Department")
    image = fields.Image("Photo")
    aadhar = fields.Image("Aadhar")

    _sql_constraints = [
        ("department_uniq", "UNIQUE(department)", "You cannot repeat same Department")
    ]
