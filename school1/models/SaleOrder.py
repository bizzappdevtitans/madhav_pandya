from odoo import fields, models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_description = fields.Many2one('student',"Invoice Description")
    # new_field = fields.Char("New field1")
    confirmed_field1=fields.Many2one('student',"field1")
    delivery_description= fields.Text("Delivery Description")
    projectt= fields.Char("Project")
    taskk= fields.Char("Task Description")



    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals["invoice_description"] = self.invoice_description
        return invoice_vals



class AccountAnalyticAccount(models.Model):
    _inherit="account.analytic.account"


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_type = fields.Selection(selection_add=[("partner", "Partners")])


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    field1 = fields.Many2one("student", 'yoo')


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_description = fields.Text('Delivery Description')








class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_description = fields.Many2one("student","Invoice Description")







class StockRuleInherit(models.Model):
    _inherit = 'stock.rule'








class Project(models.Model):
    _inherit="project.project"
    projectt= fields.Char("Project")
    purchase_orders_count=fields.Char("project Description")



class ProjectTask(models.Model):
    _inherit = "project.task"
    taskk= fields.Char("Task Description")









