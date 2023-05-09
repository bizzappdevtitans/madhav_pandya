import requests

from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    external_id = fields.Char("External Id")
    api_key = fields.Char("Api key")
    token = fields.Char("Token Key")

    def update_the_project(self):
        """Method updates the project if any updation is done in trello later on"""
        url = "https://api.trello.com/1/boards/%s/?key=%s&token=%s" % (
            self.external_id,
            self.api_key,
            self.token,
        )
        boards = requests.get(url)
        boards_values = boards.json()
        project = self.env["project.project"].search(
            [("external_id", "=", self.external_id)], limit=1
        )
        if project:
            project.write({"name": boards_values.get("name")})
        url_list = "https://api.trello.com/1/boards/%s/lists?key=%s&token=%s" % (
            self.external_id,
            self.api_key,
            self.token,
        )
        stage_response = requests.get(url_list)
        stage_data = stage_response.json()

        # Create Odoo stages for each Trello list
        project_stage_obj = self.env["project.task.type"]
        stage_mapping = {}
        for trello_list in stage_data:
            exist_stage = project_stage_obj.search(
                [("name", "=", trello_list.get("name"))], limit=1
            )
            if exist_stage:
                stage = exist_stage.write({"name": trello_list.get("name")})
                stage_mapping[trello_list.get("id")] = exist_stage.id
            else:
                stage = project_stage_obj.create({"name": trello_list.get("name")})
                stage_mapping[trello_list.get("id")] = stage.id

        url_task = "https://api.trello.com/1/boards/%s/cards/?key=%s&token=%s" % (
            self.external_id,
            self.api_key,
            self.token,
        )
        reponse_task = requests.get(url_task)
        response_data = reponse_task.json()

        # Create all tasks
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
                    "project_id": project.id,
                }
                exist_task.write(task_values)

            else:
                task_values = {
                    "name": tasks_vals.get("name"),
                    "description": tasks_vals.get("desc"),
                    "external_id": tasks_vals.get("id"),
                    "stage_id": stage_mapping[tasks_vals.get("idList")],
                    "project_id": project.id,
                }
                self.env["project.task"].create(task_values)
