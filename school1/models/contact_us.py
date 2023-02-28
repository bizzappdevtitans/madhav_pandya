from odoo import fields, models


class contact_us(models.Model):
    _name = "contact_us"
    _description = "Contact Us"

    name = fields.Char(string="Name")
    LastName = fields.Char(string="Last Name")
    ContactNo = fields.Char("ContactNO")
    email = fields.Char("email")
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

    color = fields.Integer(string="Your favourite colour")


class mail_us(models.Model):
    _name = "mail_us"
    _description = "mail_us"

    name = fields.Char("Enter your name")
    address = fields.Text("Enter your Address")
    ContactNo = fields.Char("Enter your Contact no")
    email = fields.Char("Enter your email")
    subject = fields.Char("subject")
    message = fields.Text("Message*")
