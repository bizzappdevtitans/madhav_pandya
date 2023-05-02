from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    external_id = fields.Char("External Id")
