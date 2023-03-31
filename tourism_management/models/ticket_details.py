from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class TicketDetails(models.Model):
    _name= "ticket_details"
    _description= "Ticket Details"


    reference_no= fields.Many2one(comodel_name="tour",string="Reference No")
    tour_name=fields.Selection(related="reference_no.tour_name", string="Tour Name")
    customer= fields.Many2one(comodel_name="res.partner", string="Customer")
    sales_person= fields.Many2one(comodel_name="res.users", string="Sales Person")
    tax_excluded= fields.Float(string="Tax Excluded")
    tax= fields.Float(string="Tax")
    total= fields.Float(string="Total", compute="_compute_total")


    @api.depends("tax_excluded", "tax")
    def _compute_total(self):
        """compute the total value by adding tax"""
        for rec in self:
            rec.update({"total": rec.tax_excluded + rec.tax})

