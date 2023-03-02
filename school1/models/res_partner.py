from odoo import fields, models,api


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_type = fields.Selection(selection_add=[("partner", "Partners")])
