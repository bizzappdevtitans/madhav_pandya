from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class PackageInfo(models.Model):
    _name = "package_info"
    _description = "Tour Packages"
    _rec_name = "country"

    country = fields.Many2one("res.country", string="Country")
    package_info_ids = fields.One2many(
        comodel_name="tour_packages", inverse_name="package_details_ids"
    )

    tour_id = fields.Many2one("tour")
