from odoo import api, fields, models


class teacher(models.Model):
    _name = "teacher"
    _description = "Teacher Information"

    name = fields.Char(string="Teacher Name", help="Enter your Name")
    LastName = fields.Char(string="Last name", help="Enter your Last Name")
    ContactNo = fields.Char("ContactNO", help="Enter your Contactno")
    Address = fields.Char("Address", help="Enter your Address")
    email = fields.Char("email")
    image = fields.Image(string="image")

    subject = fields.Char("Subject")

    leave = fields.Text("note")
    leave1 = fields.Text("note2")

    degree = fields.Selection([("phd", "PHD"), ("mphil", "MPhil"), ("mca", "MCA")])

    namee_ids_t = fields.Many2many("student", string="Students")

    appointment_count = fields.Integer(string="Student Count", compute="compute_count")

    # this counts the total number of teachers and will show on smart buuttons
    def compute_count(self):
        for record in self:
            record.appointment_count = self.env["teacher"].search_count(
                [("namee_ids_t", "=", self.id)]
            )

    # this will redirect to the records after clicking the smart button
    def action_open_appointments(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Students",
            "view_mode": "tree",
            "res_model": "student",
            "domain": [("id", "in", self.namee_ids_t.ids)],
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

    def action_open_appointment(self):
        print("Madhav Pandya")
        return {
            "effect": {
                "fadeout": "slow",
                "message": "BELEIVE IN YOURSELF",
                "type": "rainbow_man",
            }
        }


class faculties(models.Model):
    _name = "faculties"
    _description = "our faculties"
