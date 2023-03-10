from odoo import fields, api, models
from odoo.exceptions import ValidationError


class Admission(models.Model):
    _name = "admission"
    _description = "admission"

    name = fields.Char(string="Name", copy="False")
    lastname = fields.Char(string="Last Name")
    contact_no = fields.Char(string="contact_no")
    standard = fields.Char(string="Which standard:")
    pr_standard = fields.Float(string="Previous Standard Percentage%")

    _sql_constraints = [
        (
            "name_uniq",
            "check(Length(contact_no)=10)",
            "You can't enter less than 10 digits and more than 10 digits",
        )
    ]

    def copy(self, default={}):
        """This will return the name, Madhav whenever we try to duplicate the record"""
        default["name"] = "Madhav"
        print("self recordset", self)
        rtn = super(Admission, self).copy(default=default)
        print("return statement", rtn)
        return rtn
