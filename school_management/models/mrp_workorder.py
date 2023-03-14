from odoo import fields, models


class MrpWorkOrder(models.Model):
    _inherit = "mrp.workorder"
    manufacture = fields.Char("Manufacturing")
