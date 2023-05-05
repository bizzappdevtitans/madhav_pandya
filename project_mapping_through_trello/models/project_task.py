from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    external_id = fields.Char("External Id")
