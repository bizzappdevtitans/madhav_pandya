from odoo import fields, api, models
from odoo.exceptions import ValidationError, UserError


class StudentAppointment(models.Model):
    _name = "student_appointment"
    _description = "Student Appointment"
    _rec_name = "ref"

    name = fields.Char(string="Sudent Name")
    lastname = fields.Char(string="Last name", related="name_id.lastname")
    contact_no = fields.Char(string="contact_no")
    address = fields.Char(string="address")
    # email=fields.Char(string='email')
    booking_date = fields.Date(string="Appointment Date")
    name_id = fields.Many2one(comodel_name="student", string="Name_id")
    address_lines_ids = fields.One2many(
        "appointment.prescription.lines", "address_id", string="address Lines"
    )
    age = fields.Char(string="Age", related="name_id.age")
    email = fields.Char("email", related="name_id.email")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], related="name_id.gender"
    )

    teacher_id= fields.Many2one(comodel_name="teacher", string="Teacher")

    image = fields.Image(string="Image")
    aadhar = fields.Image("Aadhar")
    ref = fields.Char(string="Reference")

    category = fields.Selection(
        [("general", "General"), ("other", "Others")],
        string="Category",
        default="general",
    )

    _sql_constraints = [
        (
            "name_id_unique",
            "UNIQUE(name_id)",
            "You cannot repeat same name_id which already exist",
        )
    ]

    _sql_constraints = [
        (
            "name_uniq",
            "check(Length(contact_no)=10)",
            "You can't enter less than 10 digits and more than 10 digits",
        )
    ]



    def action_notify(self):
        message = {
       'type': 'ir.actions.client',
       'tag': 'display_notification',
       'params': {
           'title': ('Warning!'),
           'message':"Your appointment",
           'sticky': False,
         }
            }
        return message

    def action_share_whatsapp(self):
        if not self.name_id.contact_no:
            raise ValidationError("Students having no phone number")
        message = "Hi, %s" % self.lastname
        whatsapp_api_url = "https://web.whatsapp.com/send?phone=" + self.contact_no +"&text=" +message

        return {"type": "ir.actions.act_url", "target": "url", "url": whatsapp_api_url}

    def action_confirm(self):
        for rec in self:
            students = self.env["student"].search_count([("gender", "=", "male")])
            print("students", students)

    def action_confirm(self):
        for rec in self:
            students = self.env["student"].browse(1)
            print("students", students.name)


class AddressLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "AddressLines"

    address_id = fields.Many2one(comodel_name="student_appointment", string="Address")
