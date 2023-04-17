from odoo import fields, models


class Alumni(models.Model):
    _name = "alumni"
    _description = "Alumni Students"

    name = fields.Char("Name", help="Enter your name here")
    batch = fields.Selection(
        [("2002", "2002-05"), ("2005", "2005-08"), ("2008", "2008-11")],
        help="Enter your batch here",
    )
    company = fields.Char("Current Company", help="Enter your company name")
    position = fields.Char("Current Position", help="Enter your current position here")
