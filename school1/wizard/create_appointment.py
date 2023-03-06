from odoo import fields,models


class CreateAppointmentWizard(models.TransientModel):
    _name="create.appointment.wizard"
    _description="Create Appointment Wizard"



    name= fields.Char("Name")


    def action_create(self):
        print("\nn\nButton clicked")



