from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    field_id = fields.Many2one("student", "Field value")
    new_field = fields.Char("New or Refurbished")

    def _timesheet_create_project_prepare_values(self):
        """Returns the value from sale.order to project.project model"""
        values = super(SaleOrderLine, self)._timesheet_create_project_prepare_values()
        values.update({"project": self.order_id.project})
        return values

    def _timesheet_create_task_prepare_values(self, project):
        """Returns the value from sale.order to project.task model"""
        values = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(
            project
        )
        values.update({"task": self.order_id.task})
        return values
