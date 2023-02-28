from odoo import fields, models,api


class registration(models.Model):
    _name = "registration"
    _description = "Registration"

    name = fields.Char("Name")
    standard = fields.Char("Standard")
    event = fields.Selection([("sports", "Sports Day"), ("annual_day", "Annual day")])

    def action_confirm(self):
        for rec in self:
            students = self.env["registration"].browse(1)
            print("students", students.name)


    def default_get(self, fields):
        res = super(registration, self).default_get(fields)
        res["event"] = "annual_day"
        res["name"] = "Madhav"
        return res


    def some_fuction(self):
        self.ensure_one()


# from odoo import fields, models


# class saleorder(models.Model):
#     _inherit = "sale.order"

#     dada = fields.Char(string="New field")
