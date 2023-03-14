from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class Result(models.Model):
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

    state = fields.Selection(
        [
            ("pass", "Passed"),
            ("fail", "Failed"),
            ("promoted", "Congratulations,"),
        ],
        string="Result",
        compute="_compute_pass",
    )

    record = fields.Char("Total Records", readonly=True)

    @api.depends("percent")
    def _compute_pass(self):
        """This function will update whether student is passed or Failed"""
        for rec in self:
            if rec.percent > 35:
                rec.update({"state": "pass"})
            else:
                rec.update({"state": "fail"})

    @api.model
    def count_records(self):
        total_len = self.env["result"].search_count([("state", "=", "pass")])
        total_records = self.env["result"].update({"record": "self.total_len"})
        print("\n\ntotal records", total_len)

    def action_done(self):
        for rec in self:
            rec.state = "promoted"

    @api.depends("sub1", "sub2", "sub3", "sub4")
    def _compute_total(self):
        """compute the total marks of all 4 subjects"""
        for rec in self:
            rec.update({"total": rec.sub1 + rec.sub2 + rec.sub3 + rec.sub4})

    @api.depends("total")
    def _compute_percent(self):
        """compute the percentage according to the total marks"""
        for rec in self:
            rec.update({"percent": (rec.total * 100) / 400})

    @api.constrains("sub1")
    def _check_something(self):
        """Will raise error if the marks is entered more than 100 in subject 1"""
        for record in self:
            if record.sub1 > 100:
                raise ValidationError("You cant enter more than 100")

    def unlink(self):
        """Error will be raised whenever total is more than
        300 and if person will try to delete it"""
        for stud in self:
            if stud.total > 300:
                raise UserError("You cant delete the result")
        rtn = super(result, self).unlink()
        print("Return Statement", rtn)
        return rtn

    def action_url(self):
        return {"type": "ir.actions.act_url", "url": "https://www.gturesults.in/"}

    @api.model
    def create(self, vals):
        """Returns the unique sequence number whenever the form is created"""
        if vals.get("reference_no", ("New")) == ("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code("result") or _(
                "New"
            )
        res = super(Result, self).create(vals)
        return res
