from odoo import fields, models


class ContactUs(models.Model):
    _name = "contact_us"
    _description = "Contact Us"

    name = fields.Char(string="Name")
    lastname = fields.Char(string="Last Name")
    contact_no = fields.Char("contact_no")
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


class MailUs(models.Model):
    _name = "mail_us"
    _description = "mail_us"

    name = fields.Char("Enter your name")
    address = fields.Text("Enter your Address")
    contact_no = fields.Char("Enter your Contact no")
    email = fields.Char("Enter your email")
    subject = fields.Char("subject")
    message = fields.Text("Message*")
