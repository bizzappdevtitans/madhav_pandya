from odoo import fields, api, models
from odoo.exceptions import UserError


class toppers(models.Model):
    _name = "toppers"
    _description = "toppers"
    # _inherit= 'sale.order'

    name_id = fields.Many2one(comodel_name="student", string="Name_id")
    standard = fields.Selection(
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

    # confirmed_user_id=fields.Many2one('res.users',string="Confirm User")

    scored = fields.Float("Percentage Scored", related="name_id.percentage")

    image = fields.Image("Photo", related="name_id.image")

    _sql_constraints = [
        ("name_uniq", "UNIQUE(standard)", "You cannot repeat same standard!")
    ]

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if name_id:
            args += [
                ("standard", operator, name_id),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
