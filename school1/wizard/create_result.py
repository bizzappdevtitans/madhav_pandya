from odoo import fields,models


class CreateResultWizard(models.TransientModel):
    _name="create.result.wizard"
    _description="Create Result Wizard"



    name= fields.Char("Name")


    def action_create(self):
        print("\nn\nButton clicked")



