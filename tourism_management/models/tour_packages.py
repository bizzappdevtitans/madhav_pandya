from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class TourPackages(models.Model):
    _name= 'tour_packages'
    _description='Tour Packages'



    packages= fields.Char(string="International Packages")

    package_details_ids= fields.Many2one("package_info")
    duration= fields.Char(string="Duration")
    price= fields.Char(string="Price*")
    inclusions= fields.Text(string="Inclusions")

    def action_packages_details(self):
        """This will redirect to new form view after clicking details button in tour_packages_details"""
        return{
        'res_model': 'tour_packages_details',
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'view_id':  self.env.ref('tourism_management.tour_packages_details_view').id
        }


class TourPackagesDetails(models.Model):
    _name= 'tour_packages_details'
    _description='Tour Packages'






