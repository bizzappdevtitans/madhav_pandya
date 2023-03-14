from odoo import fields, models, api


class Registration(models.Model):
    _name = "registration"
    _description = "Registration"

    name = fields.Char("Name")
    standard = fields.Char("Standard")
    event = fields.Selection([("sports", "Sports Day"), ("annual_day", "Annual day")])

    def default_get(self, fields):
        """returns the default value whenever one try to create the new form"""
        res = super(Registration, self).default_get(fields)
        res["event"] = "annual_day"
        res["name"] = "Madhav"
        return res
