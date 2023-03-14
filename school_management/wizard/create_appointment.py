from odoo import fields, models


class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    name = fields.Char("Name")
    contact_no = fields.Char(string="contact_no")
    lastname = fields.Char(string="Lastname")
    booking_date = fields.Date(string="Appointment Date")

    def create_form(self):
        """This will create new form from wizard"""
        vals = {
            "name": self.name,
            "contact_no": self.contact_no,
        }
        res_id = self.env["student_appointment"].create(vals)

        values = {
            "name": ("Student Appointment"),
            "view_mode": "form",
            "res_model": "student_appointment",
            "target": "current",
            "type": "ir.actions.act_window",
            "res_id": res_id.id,
        }

        return values

    def create_field(self):
        """This will update the form value from wizard"""
        active_id = self._context.get("active_id")
        upd_vals = self.env["student_appointment"].browse(active_id)
        vals = {
            "name": self.name,
            "contact_no": self.contact_no,
            "lastname": self.lastname,
            "booking_date": self.booking_date,
        }
        upd_vals.write(vals)
