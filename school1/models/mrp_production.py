from odoo import fields, models


class MrpProduction(models.Model):
    _inherit="mrp.production"
    manufact=fields.Char("Manufacturing Info")
