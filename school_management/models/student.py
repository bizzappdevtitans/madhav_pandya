from datetime import date
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class Student(models.Model):
    _name = "student"
    _description = "Student Information"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Student Name", tracking=True, help="Enter your name here"
    )
    lastname = fields.Char("Last Name")
    contact_no = fields.Char("contact_no", help="Enter your Contact No here")
    address = fields.Char("address", help="Enter your address here")
    age = fields.Char(string="Age", help="Enter your age here")
    email = fields.Char("email", help="Enter your Email here", copy="false")

    _sql_constraints = [
        ("name_uniq", "UNIQUE (email)", "You cannot have same email!"),
        (
            "name_notnull",
            "CHECK(name is NOT NULL)",
            "You cannot leave blank name field",
        ),
    ]

    date_of_birth = fields.Date(
        string="Date of birth", help="Enter your Date of Birth here"
    )
    image = fields.Image(string="Image")

    leave = fields.Text("note")
    reason = fields.Text("note2")

    reference_no = fields.Char(
        string="Order Reference",
        required=True,
        readonly=True,
        default=lambda self: ("New"),
    )

    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], string="Gender", default="male"
    )

    message_follower = fields.Char("Enter the message here")

    course = fields.Float(string="Course completed")
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")
    fee = fields.Monetary(string="fee")
    total_fees = fields.Float(
        string="total_fees",
        help="This is fee field you have to add your whole year fees here",
    )

    name_ids = fields.Many2many(comodel_name="teacher", string="Teachers")

    result_ids = fields.Many2many(comodel_name="result", string="results")

    def action_open_appointmentss(self):
        """Returns the result.model view from the smart button"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "student",
            "view_mode": "tree",
            "res_model": "result",
            "domain": [("id", "in", self.result_ids.ids)],
            "context": "{'create': 'false'}",
        }

    appointment_count = fields.Integer(string="Teacher Count", compute="compute_count")
    appointment_count1 = fields.Integer(string="Result Count", compute="compute_countt")

    def compute_countt(self):
        """Count the number of students and shows the count value on smart button"""
        for record in self:
            record.appointment_count1 = self.env["student"].search_count(
                [("result_ids", "=", self.id)]
            )

    percentage = fields.Float("Percentage")

    state = fields.Selection(
        [
            ("draft", "25%"),
            ("confirm", "75%"),
            ("done", "100"),
            ("cancelled", "0%"),
        ],
        default="draft",
        string="Course Status",
    )

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

    progress = fields.Integer(string="Course Completed", compute="_compute_progress")

    parent = fields.Char("Parent")
    marital_status = fields.Selection(
        [("married", "Married"), ("unmarried", "Unmarried")], string="Marital Status"
    )
    partner_name = fields.Char("Partner Name")

    def compute_count(self):
        """this counts the total number of teachers and will show on smart buuttons"""
        for record in self:
            record.appointment_count = self.env["student"].search_count(
                [("name_ids", "=", self.id)]
            )

    @api.depends("state")
    def _compute_progress(self):
        """This measure the state"""
        for rec in self:
            if rec.state == "draft":
                progress = 25
            elif rec.state == "cancelled":
                progress = 0
            elif rec.state == "confirm":
                progress = 75
            elif rec.state == "done":
                progress = 100
            rec.progress = progress

    @api.onchange("date_of_birth")
    def onchange_date_of_birth(self):
        """This counts the age according to the date_of_birth"""
        for res in self:
            today = date.today()
            if res.date_of_birth:
                res.age = today.year - res.date_of_birth.year

    def write(self, values):
        print("Values.....", values)
        rtn = super(student, self).write(values)
        return rtn

    def action_open_appointments(self):
        """this will redirect to the records after clicking the smart button"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Students",
            "view_mode": "tree",
            "res_model": "teacher",
            "domain": [("id", "in", self.name_ids.ids)],
            "context": "{'create': 'false'}",
        }

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_done(self):
        """if state is 100% in record, and if we try to delete than this will raise an error."""
        if any(batch.state == "done" for batch in self):
            raise UserError("You cannot delete, because state is at 100%")

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        """By typing email and lastname also we can fetch the records.."""

        args = list(args or [])
        if name:
            args += [
                "|",
                "|",
                ("name", operator, name),
                ("lastname", operator, name),
                ("email", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def default_get(self, fields):
        """Returns the default value when someone try to create the new form"""
        res = super(Student, self).default_get(fields)
        res["gender"] = "female"
        res["name"] = "Madhav"
        return res

    @api.model
    def create(self, vals):
        """Returns the unique sequence number whenever new form is created"""
        if vals.get("reference_no", ("New")) == ("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code("student") or _(
                "New"
            )
        res = super(Student, self).create(vals)
        return res

    _sql_constraints = [
        (
            "name_uniq",
            "check(Length(contact_no)=10)",
            "You can't enter less than 10 digits and more than 10 digits",
        )
    ]
