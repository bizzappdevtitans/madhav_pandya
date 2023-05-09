import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class CreateProjectWizard(models.TransientModel):
    _name = "create.project.wizard"
    _description = "Create Project through Wizard"

    project_option = fields.Selection(
        [("single", "Import single project"), ("all", "Import all Project")],
        string="Select option",
    )

    project_importer = fields.Char(string="Project Importer")
    api_key = fields.Char("Enter Api key")
    token = fields.Char("Enter Token")
    workspace = fields.Char("Workspace id")

    def import_data_from_trello(self):
        url = "https://api.trello.com/1/boards/%s/?key=%s" "&token=%s" % (
            self.project_importer,
            self.api_key,
            self.token,
        )
        boards = requests.request("GET", url)
        # print("\n\n\n",boards)
        # print("\n\n\n",boards.status_code)
        # print("\n\n\n\n",boards_values.status_code)
        if boards.status_code != 200:
            raise (_(ValidationError("Invalid api or token")))
        boards_values = boards.json()
        # print("\n\n\n\n", boards_values)
        vals = self.env["project.project"].search(
            [("external_id", "=", self.project_importer)]
        )
        if not vals:
            vals = (
                self.env["project.project"]
                .sudo()
                .create(
                    {
                        "external_id": boards_values.get("id"),
                        "name": boards_values.get("name"),
                        "api_key": self.api_key,
                        "token": self.token,
                    }
                )
            )

        url_list = "https://api.trello.com/1/boards/%s/lists?key=%s&token=%s" % (
            self.project_importer,
            self.api_key,
            self.token,
        )
        stage_response = requests.request("GET", url_list)

        if stage_response.status_code != 200:
            raise (_(ValidationError("Invalid api or token")))

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
            self.project_importer,
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
            # print("\n\n\n\n\n", tasks_vals.get("id"))
            if exist_task:
                task_values = {
                    "name": tasks_vals.get("name"),
                    "description": tasks_vals.get("desc"),
                    "external_id": tasks_vals.get("id"),
                    "stage_id": stage_mapping[tasks_vals.get("idList")],
                    "project_id": vals.id,
                }
                exist_task.write(task_values)

            else:
                task_values = {
                    "name": tasks_vals.get("name"),
                    "description": tasks_vals.get("desc"),
                    "external_id": tasks_vals.get("id"),
                    "stage_id": stage_mapping[tasks_vals.get("idList")],
                    "project_id": vals.id,
                }
                self.env["project.task"].create(task_values)

    def import_all_project_from_trello(self):
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
                    self.env["project.project"]
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
                # print("\n\n\n\nnew", tasks_vals.get("id"))

                if exist_task:
                    task_values = {
                        "name": tasks_vals.get("name"),
                        "description": tasks_vals.get("desc"),
                        "external_id": tasks_vals.get("id"),
                        "stage_id": stage_mapping[tasks_vals.get("idList")],
                        "project_id": vals.id,
                    }
                    exist_task.write(task_values)

                else:
                    task_values = {
                        "name": tasks_vals.get("name"),
                        "description": tasks_vals.get("desc"),
                        "external_id": tasks_vals.get("id"),
                        "stage_id": stage_mapping[tasks_vals.get("idList")],
                        "project_id": vals.id,
                    }
                    self.env["project.task"].create(task_values)
        return {
            "name": "Project Kanban",
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "view_mode": "form",
            "res_id": vals.id,
        }
