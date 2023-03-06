from odoo import fields, models


class MrpWorkOrder(models.Model):
    _inherit = "mrp.workorder"
    manufact = fields.Char("Manufacturing")
