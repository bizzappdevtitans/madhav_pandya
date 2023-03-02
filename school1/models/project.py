from odoo import fields,models



class Project(models.Model):
    _inherit="project.project"
    projectt= fields.Char("Project")
    purchase_orders_count=fields.Char("project Description")
