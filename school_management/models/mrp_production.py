from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"
    manufacture = fields.Char("Manufacturing Info")
