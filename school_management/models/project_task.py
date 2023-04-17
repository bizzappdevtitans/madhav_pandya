from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"
    task = fields.Char("Task Description")
