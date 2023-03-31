from odoo import fields, models


class UpdateBookingAccomodationWizard(models.TransientModel):
    _name = "update.booking.accomodation.wizard"
    _description = "Update Booking Accomodation Wizard"



    date_in= fields.Date("Check in")
    date_out= fields.Date("Check out")

    room_type=fields.Selection([('duplex','Duplex room'), ('delux', 'Delux Room'),('delux_jac','Delux Room with jackuzi')])



    def create_field(self):
        """This will update the form value from wizard"""
        active_id = self._context.get("active_id")
        upd_vals = self.env["booking_accomodation"].browse(active_id)
        vals = {
            "date_in": self.date_in,
            "date_out": self.date_out,
            "room_type": self.room_type,
        }
        upd_vals.write(vals)
