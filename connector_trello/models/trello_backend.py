import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class TrelloBackend(models.Model):
    _name = "trello.backend"
    _description = "Trello Backend"

    api_key = fields.Char("Api Key")
    token = fields.Char("Token")
    workspace = fields.Char("Enter Workspce id")
    external_id = fields.Char("external_id")

    def import_project_from_trello(self):
        url_projects = (
            "https://api.trello.com/1/organizations/%s/boards/?key=%s&token=%s"
            % (self.workspace, self.api_key, self.token)
        )
        response_all_project = requests.request("GET", url_projects)
        if response_all_project.status_code != 200:
            raise (_(ValidationError("Invalid api or token")))
        projects_data = response_all_project.json()
        project_obj = self.env["project.project"]
        for projects in projects_data:
            vals = project_obj.search(
                [("external_id", "=", projects.get("id"))], limit=1
            )
            if vals:
                vals.write({"name": projects.get("name")})
            else:
                vals = (
                    self.env["trello.project.project"]
                    .sudo()
                    .create(
                        {
                            "external_id": projects.get("id"),
                            "name": projects.get("name"),
                            "api_key": self.api_key,
                            "token": self.token,
                            "odoo_id": vals.id,
                        }
                    )
                )

    def import_stage_from_trello(self):
        url_projects = (
            "https://api.trello.com/1/organizations/%s/boards/?key=%s&token=%s"
            % (self.workspace, self.api_key, self.token)
        )
        response_all_project = requests.request("GET", url_projects)
        if response_all_project.status_code != 200:
            raise (_(ValidationError("Invalid api or token")))
        projects_data = response_all_project.json()
        project_obj = self.env["project.project"]
        for projects in projects_data:
            vals = project_obj.search(
                [("external_id", "=", projects.get("id"))], limit=1
            )
            if vals:
                vals.write({"name": projects.get("name")})
            else:
                vals = (
                    self.env["trello.project.project"]
                    .sudo()
                    .create(
                        {
                            "external_id": projects.get("id"),
                            "name": projects.get("name"),
                            "api_key": self.api_key,
                            "token": self.token,
                            "odoo_id": vals.id,
                        }
                    )
                )

            url_list = "https://api.trello.com/1/boards/%s/lists?key=%s&token=%s" % (
                projects.get("id"),
                self.api_key,
                self.token,
            )
            # print("\n\n\n\n", projects.get("name"))
            stage_response = requests.get(url_list)
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

    def import_task_from_trello(self):
        url_projects = (
            "https://api.trello.com/1/organizations/%s/boards/?key=%s&token=%s"
            % (self.workspace, self.api_key, self.token)
        )
        response_all_project = requests.request("GET", url_projects)
        if response_all_project.status_code != 200:
            raise (_(ValidationError("Invalid api or token")))
        projects_data = response_all_project.json()
        project_obj = self.env["project.project"]
        for projects in projects_data:
            vals = project_obj.search(
                [("external_id", "=", projects.get("id"))], limit=1
            )
            if not vals:
                vals = (
                    self.env["trello.project.project"]
                    .sudo()
                    .create(
                        {
                            "external_id": projects.get("id"),
                            "name": projects.get("name"),
                            "api_key": self.api_key,
                            "token": self.token,
                        }
                    )
                )

            url_list = "https://api.trello.com/1/boards/%s/lists?key=%s&token=%s" % (
                projects.get("id"),
                self.api_key,
                self.token,
            )
            stage_response = requests.request("GET", url_list)
            if stage_response.status_code != 200:
                raise (_(ValidationError("Invalid api or token")))
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
                projects.get("id"),
                self.api_key,
                self.token,
            )
            reponse_task = requests.request("GET", url_task)
            if reponse_task.status_code != 200:
                raise (_(ValidationError("Invalid api or token")))
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
                        "project_id": vals.id,
                    }
                    exist_task.write(task_values)
                    # print("\n\n\n", exist_task.id)

                else:
                    task_values = {
                        "name": tasks_vals.get("name"),
                        "description": tasks_vals.get("desc"),
                        "external_id": tasks_vals.get("id"),
                        "stage_id": stage_mapping[tasks_vals.get("idList")],
                        "project_id": vals.id,
                        "odoo_id": exist_task.id,
                    }
                    exist_task = self.env["trello.project.task"].create(task_values)
                    # print("\n\n\n", exist_task.id)
