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



    def _prepare_analytic_account_data(self, prefix):
        vals=super(SaleOrder,self)._prepare_analytic_account_data()
        vals['projectt']= self.projectt
        return vals

class AccountAnalyticAccount(models.Model):
    _inherit="account.analytic.account"
    projectt= fields.Char("Project")


    # def _timesheet_create_project_prepare_values(self):
    #     print("\n\nprojecttttt running")
    #     vals=super(SaleOrder,self)._timesheet_create_project_prepare_values()
    #     vals['projectt']=self.projectt
    #     return  vals


    # def _timesheet_create_task_prepare_values(self):
    #     print("\n\n Taskk runningggggg........")
    #     vals=super(SaleOrder,self)._timesheet_create_task_prepare_values()
    #     vals['taskk']=self.taskk
    #     return  vals






class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    field1=fields.Many2one("student","Field value")
    new_field = fields.Char("New or Refurbished")










class ResPartner(models.Model):
    _inherit = "res.partner"

    company_type = fields.Selection(selection_add=[("partner", "Partners")])


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    field1 = fields.Many2one("student", 'yoo')


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_description = fields.Text('Delivery Description')


    # def _prepare_picking_vals(self, partner, picking_type, location_id, location_dest_id):
    #     return {
    #         'partner_id': partner.id if partner else False,
    #         'user_id': False,
    #         'picking_type_id': picking_type.id,
    #         'move_type': 'direct',
    #         'location_id': location_id,
    #         'location_dest_id': location_dest_id,
    #     }


    # def _prepare_picking_vals(self,partner,picking_type,location_id,location_dest_id):
    #     invoice_vals = super(StockPicking, self)._prepare_picking_vals()
    #     invoice_vals["delivery_description"]= self.delivery_description
    #     return invoice_vals








class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_description = fields.Many2one("student","Invoice Description")





class StockMove(models.Model):
    _inherit = "stock.move"

    field1 = fields.Text("New field")
    delivery_description = fields.Text('Delivery Description')

    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        print("Madhav.............")
        vals['delivery_description'] = self.sale_line_id.order_id.delivery_description
        return vals

class StockRuleInherit(models.Model):
    _inherit = 'stock.rule'




class SaleAdvancePaymentInv(models.TransientModel):
    _inherit="sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        inv_obj = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        inv_obj["invoice_description"]= order.invoice_description
        return inv_obj



class Project(models.Model):
    _inherit="project.project"
    project_id= fields.Many2one("account.analytic.account")

    projectt= fields.Char("Project",related="project_id.projectt")

    # def _timesheet_create_project_prepare_values(self):
    #     vals=super(SaleOrder,self)._timesheet_create_project_prepare_values()
    #     vals['projectt']=self.projectt
    #     return  vals


class ProjectTask(models.Model):
    _inherit = "project.task"
    taskk= fields.Char("Task Description")

    # def _timesheet_create_task_prepare_values(self):
    #     vals=super(SaleOrder,self)._timesheet_create_task_prepare_values()
    #     vals['taskk']=self.taskk
    #     return  vals












