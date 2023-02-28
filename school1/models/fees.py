from odoo import fields, api, models


class fees(models.Model):
    _name = "fees"
    _description = "Fees Structure"

    department = fields.Selection(
        [
            ("std1", "Standard 1st"),
            ("std2", "Standard 2nd"),
            ("std3", "Standard 3rd"),
            ("std4", "Standard 4th"),
            ("std5", "Standard 5th"),
            ("std6", "Standard 6th"),
            ("std7", "Standard 7th"),
            ("std8", "Standard 8th"),
            ("std9", "Standard 9th"),
            ("std10", "Standard 10th"),
            ("std11", "Standard 11th"),
            ("std12", "Standard 12th"),
        ]
    )
    sem1 = fields.Float("Sem 1")
    sem2 = fields.Float("Sem 2")
    total = fields.Float("Total Fees", compute="_compute_total_fees")

    _sql_constraints = [
        (
            "name_uniq",
            "UNIQUE(department)",
            "This department already exist in fee structure",
        )
    ]

    @api.depends("sem1", "sem2")
    def _compute_total_fees(self):
        for rec in self:
            rec.update({"total": rec.sem1 + rec.sem2})
