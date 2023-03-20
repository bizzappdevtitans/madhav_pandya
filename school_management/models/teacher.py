from odoo import api, fields, models


class Teacher(models.Model):
    _name = "teacher"
    _description = "Teacher Information"

    name = fields.Char(string="Teacher Name", help="Enter your Name")
    lastname = fields.Char(string="Last name", help="Enter your Last Name")
    contact_no = fields.Char("contact_no", help="Enter your contact_no")
    address = fields.Char("address", help="Enter your address")
    email = fields.Char("email")
    image = fields.Image(string="image")



    subject = fields.Char("Subject")

    leave = fields.Text("note")
    reason = fields.Text("note2")

    degree = fields.Selection([("phd", "PHD"), ("mphil", "MPhil"), ("mca", "MCA")])

    name_ids = fields.Many2many(comodel_name="student", string="Students")

    appointment_count = fields.Integer(string="Student Count", compute="compute_count")

    def compute_count(self):
        """this counts the total number of teachers and will show on smart buttons"""
        for record in self:
            record.appointment_count = self.env["teacher"].search_count(
                [("name_ids", "=", self.id)]
            )

    def action_open_appointments(self):

        """this will redirect to the records after clicking the smart button"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Students",
            "view_mode": "tree",
            "res_model": "student",
            "domain": [("id", "in", self.name_ids.ids)],
            "context": "{'create': 'false'}",
        }

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        string="Status",
    )


class Faculties(models.Model):
    _name = "faculties"
    _description = "our faculties"
