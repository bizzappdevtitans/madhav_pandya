from odoo import fields, models


class UpdateTourWizard(models.TransientModel):
    _name = "update.tour.wizard"
    _description = "Update Tour Wizard"



    tour_name= fields.Selection([('dubai', 'Dubai'), ('philipines','Philipines'), ('maldives', 'Maldives')],string="Tour Name")
    tour_type= fields.Selection([('type1', 'Sightseeing Tours'), ('type2','Shore Excursion Tours')
        , ('type3', 'Adventure or Sporting Tours.')], string="Tour type")


    def create_field(self):
        """This will update the form value from wizard"""
        active_id = self._context.get("active_id")
        upd_vals = self.env["tour"].browse(active_id)
        vals = {
            "tour_name": self.tour_name,
            "tour_type": self.tour_type,
        }
        upd_vals.write(vals)

class UpdateTourIteneraryWizard(models.TransientModel):
    _name= "update.tour.itenerary.wizard"
    _description= "Update Tour Itenerary Wizard"

    tour_id= fields.Many2one("tour",string= "Customer Inquiry")
    contact_name_id= fields.Many2one("res.partner",string="Contact Name")
    email= fields.Char("Email")
    mobile= fields.Char("Contact No")

    prefer_start_date= fields.Date("Prefer Start Date")
    prefer_end_date= fields.Date("Prefer End date")


    def update_form(self):
        """This will update the form value from wizard"""
        active_id = self._context.get("active_id")
        upd_vals = self.env["tour_itenerary"].browse(active_id)
        vals = {
            "tour_id": self.tour_id,
            "contact_name_id": self.contact_name_id,
            "email": self.email,
            "mobile": self.mobile,
            "prefer_start_date": self.prefer_start_date,
            "prefer_end_date": self.prefer_end_date,
        }
        upd_vals.write(vals)

    def create_form(self):
        """This will create new form from wizard"""
        vals = {
            "tour_id": self.tour_id,
            "contact_name_id": self.contact_name_id,
        }
        res_id = self.env["tour_itenerary"].create(vals)

        values = {
            "name": ("tour_itenerary"),
            "view_mode": "form",
            "res_model": "tour_itenerary",
            "target": "current",
            "type": "ir.actions.act_window",
            "res_id": res_id.id,
        }

        return values
