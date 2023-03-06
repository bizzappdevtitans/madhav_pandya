from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    field1 = fields.Many2one("student", "Field value")
    new_field = fields.Char("New or Refurbished")
    # purchase_description=fields.Char("Purchase")

    def _timesheet_create_project_prepare_values(self):
        values = super(SaleOrderLine, self)._timesheet_create_project_prepare_values()
        values.update({"projectt": self.order_id.projectt})
        return values

    def _timesheet_create_task_prepare_values(self, project):
        values = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(
            project
        )
        values.update({"taskk": self.order_id.taskk})
        return values
