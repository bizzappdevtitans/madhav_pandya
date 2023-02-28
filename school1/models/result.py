from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class result(models.Model):
    _name = "result"
    _description = "Student Result"

    name = fields.Char(string="Name")

    sub1 = fields.Float(string="Physics", help="Enter your Physics marks here")
    sub2 = fields.Float(string="Maths", help="Enter your Maths marks here")
    sub3 = fields.Float(string="Chemistry", help="Enter your Chemistry marks here")
    sub4 = fields.Float(string="English", help="Enter your English marks here")

    total = fields.Float(
        compute="_compute_total", string="Total Marks", help="Total Marks"
    )
    percent = fields.Float(
        compute="_compute_percent", string="Your percentage", help="Percentage"
    )

    reference_no = fields.Char(
        string="Order Reference",
        required=True,
        readonly=True,
        default=lambda self: ("New"),
    )

    passing_class = fields.Char(compute="_compute_class", string="Passing Class")

    # this will count total of given four subject
    @api.depends("sub1", "sub2", "sub3", "sub4")
    def _compute_total(self):
        for rec in self:
            rec.update({"total": rec.sub1 + rec.sub2 + rec.sub3 + rec.sub4})

    # this will count the percentage on the basis of total
    @api.depends("total")
    def _compute_percent(self):
        for rec in self:
            rec.update({"percent": (rec.total * 100) / 400})

    # this will throw error if the person will enter more marks above 100
    @api.constrains("sub1")
    def _check_something(self):
        for record in self:
            if record.sub1 > 100:
                raise ValidationError("You cant enter more than 100")

    def unlink(self):
        print("self statement", self)
        for stud in self:
            if stud.total > 300:
                raise UserError("You cant delete the result")
        rtn = super(result, self).unlink()
        print("Return Statement", rtn)
        return rtn

    @api.model
    def create(self, vals):
        if vals.get("reference_no", ("New")) == ("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code("result") or _(
                "New"
            )
        res = super(result, self).create(vals)
        return res
