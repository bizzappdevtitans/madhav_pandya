from odoo import fields, models


class student_appointment(models.Model):
    _name = "student_appointment"
    _description = "Student Appointment"
    _rec_name = "ref"
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Sudent Name")
    LastName = fields.Char(string="Last name", related="name_id.LastName")
    ContactNo = fields.Char(string="ContactNO")
    Address = fields.Char(string="Address")
    # email=fields.Char(string='email')
    booking_date = fields.Date(string="Appointment Date")
    name_id = fields.Many2one(comodel_name="student", string="Name_id")
    Address_lines_ids = fields.One2many(
        "appointment.prescription.lines", "address_id", string="Address Lines"
    )
    age = fields.Char(string="Age", related="name_id.age")
    email = fields.Char("email", related="name_id.email")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], related="name_id.gender"
    )

    image = fields.Image(string="Image")
    aadhar = fields.Image("Aadhar")
    ref = fields.Char(string="Reference")

    category = fields.Selection(
        [("general", "General"), ("other", "Others")],
        string="Category",
        default="general",
    )

    # reference_field=fields.Reference([('student','Student')],string="Record")

    _sql_constraints = [
        (
            "name_id_unique",
            "UNIQUE(name_id)",
            "You cannot repeat same name_id which already exist",
        )
    ]

    def action_confirm(self):
        for rec in self:
            students = self.env["student"].search_count([("gender", "=", "male")])
            print("students", students)
            # female_students=self.env['student']. search([('gender', '=', 'female')])
            # print('female_students', female_students)

    def action_confirm(self):
        for rec in self:
            students = self.env["student"].browse(1)
            print("students", students.name)


class Address_lines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Address_lines"

    address_id = fields.Many2one("student_appointment", string="Address")
