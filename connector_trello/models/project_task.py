import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    trello_bind_ids = fields.One2many(
        comodel_name="trello.project.task", inverse_name="odoo_id", readonly=True
    )
    external_id = fields.Char("External id", related="trello_bind_ids.external_id")
    api_key = fields.Char("Api Key", related="trello_bind_ids.api_key")
    token = fields.Char("Token", related="trello_bind_ids.token")
    project_external_id = fields.Char(
        "Project External id", related="trello_bind_ids.project_external_id"
    )
    task_created_date = fields.Datetime(
        "Task Created Date", related="trello_bind_ids.task_created_date"
    )
    task_updated_date = fields.Datetime("Task Updated Date")
    internal_id = fields.Char("Internal Id")

    def update_task(self):
        url_list = "https://api.trello.com/1/boards/%s/lists?key=%s&token=%s" % (
            self.project_external_id,
            self.api_key,
            self.token,
        )
        stage_response = requests.request("GET", url_list)
        if stage_response.status_code != 200:
            raise ValidationError(_("Invalid api or token"))
        stage_data = stage_response.json()

        # Create Odoo stages for each Trello list
        project_stage_obj = self.env["project.task.type"]
        project_trello_obj = self.env["trello.project.task.type"]
        stage_mapping = {}
        for trello_list in stage_data:
            exist_stage = project_stage_obj.search(
                [("external_id", "=", trello_list.get("id"))], limit=1
            )
            if exist_stage:
                stage = exist_stage.write({"name": trello_list.get("name")})
                stage_mapping[trello_list.get("id")] = exist_stage.id
            else:
                stage = project_trello_obj.create(
                    {
                        "name": trello_list.get("name"),
                        "external_id": trello_list.get("id"),
                        "odoo_id": exist_stage.id,
                    }
                )
                stage_mapping[trello_list.get("id")] = stage.id

        url_task = "https://api.trello.com/1/boards/%s/cards/?key=%s&token=%s" % (
            self.project_external_id,
            self.api_key,
            self.token,
        )
        reponse_task = requests.request("GET", url_task)
        if reponse_task.status_code != 200:
            raise ValidationError(_("Invalid api or token"))
        response_data = reponse_task.json()
        project_task_obj = self.env["project.task"]
        for tasks_vals in response_data:
            exist_task = project_task_obj.search(
                [("external_id", "=", tasks_vals.get("id"))], limit=1
            )
            if exist_task:
                task_values = {
                    "name": tasks_vals.get("name"),
                    "description": tasks_vals.get("desc"),
                    "external_id": tasks_vals.get("id"),
                    "stage_id": stage_mapping[tasks_vals.get("idList")],
                    "task_updated_date": fields.Datetime.now(),
                }
                exist_task.write(task_values)
                # print("\n\n\n", exist_task.id)

            else:
                task_values = {
                    "name": tasks_vals.get("name"),
                    "description": tasks_vals.get("desc"),
                    "external_id": tasks_vals.get("id"),
                    "stage_id": stage_mapping[tasks_vals.get("idList")],
                    "odoo_id": exist_task.id,
                }
                exist_task = self.env["trello.project.task"].create(task_values)
