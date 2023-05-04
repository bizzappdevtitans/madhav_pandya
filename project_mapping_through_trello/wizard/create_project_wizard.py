import requests

from odoo import fields, models


class CreateProjectWizard(models.TransientModel):
    _name = "create.project.wizard"
    _description = "Create Project through Wizard"

    project_importer = fields.Char(string="Project Importer")

    def import_data_from_trello(self):
        url = (
            "https://api.trello.com/1/boards/%s/?key=d0e8e49052ffc8d9b19945eaff3fec29"
            "&token=ATTA9630a7b59094d59905fd4a97a6abff30294d5058810e97dc4b76420ca474c"
            "8e9D1B31FC7" % self.project_importer
        )
        boards = requests.get(url)
        boards_values = boards.json()
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
                    }
                )
            )

        url_list = (
            "https://api.trello.com/1/boards/%s/lists?key=d0e8e49052f"
            "fc8d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30294d505881"
            "0e97dc4b76420ca474c8e9D1B31FC7" % self.project_importer
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
            if not exist_stage:
                stage = project_stage_obj.create({"name": trello_list.get("name")})
                stage_mapping[trello_list.get("id")] = stage.id
            if exist_stage:
                stage_mapping[trello_list.get("id")] = exist_stage.id

        url_task = (
            "https://api.trello.com/1/boards/%s/cards/?key=d0e8e49052ffc8"
            "d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30294d505"
            "8810e97d"
            "c4b76420ca474c8e9D1B31FC7" % self.project_importer
        )
        reponse_task = requests.get(url_task)
        response_data = reponse_task.json()
        project_task_obj = self.env["project.task"]
        for tasks_vals in response_data:
            exist_task = project_task_obj.search(
                [("name", "=", tasks_vals.get("name"))], limit=1
            )
            if not exist_task:
                task_values = {
                    "name": tasks_vals.get("name"),
                    "description": tasks_vals.get("desc"),
                    "external_id": tasks_vals.get("idShort"),
                    "stage_id": stage_mapping[tasks_vals.get("idList")],
                    "project_id": vals.id,
                }
                self.env["project.task"].create(task_values)
            if exist_task:
                task_values = {
                    "name": tasks_vals.get("name"),
                    "description": tasks_vals.get("desc"),
                    "external_id": tasks_vals.get("idShort"),
                    "stage_id": stage_mapping[tasks_vals.get("idList")],
                    "project_id": vals.id,
                }
                self.env["project.task"].write(task_values)

    def import_all_project_from_trello(self):
        url_projects = (
            "https://api.trello.com/1/organizations/mpdstitan/boards/?key=d"
            "0e8e49052ffc8d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30294"
            "d5058810e97dc4b76420ca474c8e9D1B31FC7"
        )
        response_all_project = requests.get(url_projects)
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
                        }
                    )
                )

            url_list = (
                "https://api.trello.com/1/boards/%s/lists?key=d0e8e49052f"
                "fc8d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30294d"
                "505881"
                "0e97dc4b76420ca474c8e9D1B31FC7" % projects.get("id")
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
                if not exist_stage:
                    stage = project_stage_obj.create({"name": trello_list.get("name")})
                    stage_mapping[trello_list.get("id")] = stage.id
                if exist_stage:
                    stage_mapping[trello_list.get("id")] = exist_stage.id

            url_task = (
                "https://api.trello.com/1/boards/%s/cards/?key=d0e8e49052ffc8"
                "d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30294d50"
                "58810e97d"
                "c4b76420ca474c8e9D1B31FC7" % projects.get("id")
            )
            reponse_task = requests.get(url_task)
            response_data = reponse_task.json()
            project_task_obj = self.env["project.task"]
            for tasks_vals in response_data:
                exist_task = project_task_obj.search(
                    [("name", "=", tasks_vals.get("name"))], limit=1
                )
                if not exist_task:
                    task_values = {
                        "name": tasks_vals.get("name"),
                        "description": tasks_vals.get("desc"),
                        "external_id": tasks_vals.get("idShort"),
                        "stage_id": stage_mapping[tasks_vals.get("idList")],
                        "project_id": vals.id,
                    }
                    exist_task = self.env["project.task"].create(task_values)
                if exist_task:
                    task_values = {
                        "name": tasks_vals.get("name"),
                        "description": tasks_vals.get("desc"),
                        "external_id": tasks_vals.get("idShort"),
                        "stage_id": stage_mapping[tasks_vals.get("idList")],
                        "project_id": vals.id,
                    }
                    exist_task = self.env["project.task"].write(task_values)
