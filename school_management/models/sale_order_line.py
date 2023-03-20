from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    field_id = fields.Many2one("student", "Field value")
    product_template_id = fields.Many2one('product.template')
    weight_id=fields.Many2one(comodel_name='stock.move')
    new_field = fields.Boolean(related="product_template_id.weight_done")
    weight_measure=fields.Float("Weight Measure")

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
