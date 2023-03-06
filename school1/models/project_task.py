from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"
    taskk = fields.Char("Task Description")
