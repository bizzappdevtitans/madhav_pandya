from odoo import fields, api, models
from odoo.exceptions import ValidationError


class admission(models.Model):
    _name = "admission"
    _description = "admission"

    name = fields.Char(string="Name", copy="False")
    LastName = fields.Char(string="Last Name")
    ContactNo = fields.Char("ContactNO")
    standard = fields.Char("Which standard:")
    pr_standard = fields.Float("Previous Standard Percentage%")

    @api.constrains("ContactNO")
    def _check_something(self):
        for record in self:
            if record.ContactNo > "10":
                raise ValidationError("You cant enter more than 10 digits")

    def copy(self, default={}):
        default["name"] = "Madhav"
        print("self recordset", self)
        rtn = super(admission, self).copy(default=default)
        print("return statement", rtn)
        return rtn
