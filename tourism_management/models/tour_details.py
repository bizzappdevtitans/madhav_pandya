from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class TourDetails(models.Model):
    _name= 'tour_details'
    _description='Tour Details'


    tour_season= fields.Selection([('s1','Summer'), ('s2', 'Winter'),  ('s3', 'Monsoon')])
    start_date=  fields.Date(string="Start date")
    email= fields.Char(string="Email")
    mobile=fields.Char(string="Contact No")
    last_date_booking= fields.Date(string="Last Date")
    payment_due_date=fields.Date(string="Payment Due date")
    total_seats= fields.Integer(string="Total seats")
    available_seats= fields.Integer(string="Available seats")
    status = fields.Selection(
        [
            ("draft", "On-Hold"),
            ("confirm", "Tatkal"),
            ("done", "Confirmed"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        string="Ticket Status",
    )


    _sql_constraints = [
        (
            "email_unique",
            "UNIQUE(email)",
            "The given email is already in use",
        )
    ]


    def action_done(self):
        """This will update the status and move the state in done state"""
        for rec in self:
            rec.status = "done"


    def action_send_email(self):
        """This function send the "Happy journey" message to traveller email according to their journey start date """
        for rec in self.search([]):
            today = date.today()
            if (
                today.day == rec.start_date.day
                and today.month == rec.start_date.month
            ):
                template_id = self.env.ref(
                    "tourism_management.customer_journey_email_template"
                ).id
                template = self.env["mail.template"].browse(template_id)
                template.send_mail(rec.id, force_send=True)
                template_ids = self.env.ref("mail.channel_all_employees").id
                channel_ids = self.env["mail.channel"].browse(template_ids)
                message = ("Happy Journey")
                channel_ids.message_post(
                    body=message,
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )


    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_done(self):
        """if status  is Confirmed  in record, and if we try to delete than this will raise an error."""
        if any(batch.status == "done" for batch in self):
            raise UserError("You cannot delete, ticket is confirmed")



    def action_send_email_tickets(self):
        """This function send the "Happy journey" message to traveller email according to their journey start date """
        for rec in self.search([]):
            if (
                rec.status=='done'
            ):
                template_id = self.env.ref(
                    "tourism_management.customer_ticket_email_template"
                ).id
                template = self.env["mail.template"].browse(template_id)
                template.send_mail(rec.id, force_send=True)




