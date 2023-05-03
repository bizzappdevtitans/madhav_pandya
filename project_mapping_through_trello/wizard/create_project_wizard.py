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
        board_response = requests.get(url_list)
        board_data = board_response.json()

        # Create Odoo stages for each Trello list
        project_stage_obj = self.env["project.task.type"]
        stage_mapping = {}
        for trello_list in board_data:
            stage = project_stage_obj.create({"name": trello_list.get("name")})
            stage_mapping[trello_list.get("id")] = stage.id
            # print("\n\n\n",trello_list)
            # print("\n\n\nstage id",stage.id)

        url_task = (
            "https://api.trello.com/1/boards/%s/cards/?key=d0e8e49052ffc8"
            "d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30294d5058810e97d"
            "c4b76420ca474c8e9D1B31FC7" % self.project_importer
        )
        reponse_task = requests.get(url_task)
        response_data = reponse_task.json()
        for tasks_vals in response_data:
            task_values = {
                "name": tasks_vals.get("name"),
                "description": tasks_vals.get("desc"),
                "external_id": tasks_vals.get("idShort"),
                "stage_id": stage_mapping[tasks_vals["idList"]],
                "project_id": vals.id,
            }
            self.env["project.task"].create(task_values)

        # url_list = (
        #     "https://api.trello.com/1/boards/%s/lists?key=d0e8e49052f"
        #     "fc8d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30
        # 294d505881"
        #     "0e97dc4b76420ca474c8e9D1B31FC7"% self.project_importer
        # )

        # payload_list = {}

        # response_list = requests.request("GET", url_list, data=payload_list)
        # data_list = response_list.json()
        # vals= self.env['project.task']
        # for lists in data_list:
        #     lists_values={
        #     'name':lists.get('name')
        #     }
        #     print('\n\n\n',lists_values)
        #     values=self.env['project.task.type'].create(lists_values)
        #     vals.write({'stage_id':values.id})

    def import_task_from_trello(self):
        url_list = (
            "https://api.trello.com/1/boards/%s/lists?key=d0e8e49052f"
            "fc8d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30294d505881"
            "0e97dc4b76420ca474c8e9D1B31FC7" % self.project_importer
        )

        payload_list = {}

        response_list = requests.request("GET", url_list, data=payload_list)
        data_list = response_list.json()
        project_stage_obj = self.env["project.task.type"]
        stage_mapping = {}
        for trello_list in data_list:
            stage_name = trello_list["name"]
            stage = project_stage_obj.create({"name": stage_name})
            stage_mapping[trello_list["id"]] = stage.id

        project_task_obj = self.env["project.task"]
        for trello_card in data_list:
            task_values = {
                "name": trello_card["name"],
                "description": trello_card["desc"],
                "stage_id": stage_mapping[trello_card["idList"]],
            }
            project_task_obj.create(task_values)

        # for lists in data_list:
        #     lists_values={
        #     'name':lists.get('name')
        #     }
        #     print('\n\n\n',lists_values)
        #     values=self.env['project.task.type'].create(lists_values)
        #     vals.write({'stage_id':values.id})

        # if vals:
        #     list_type = self.env["project.task.type"].create(
        #         {"name": data_list[2].get("name")}
        #     )
        # vals.write({"stage_id": list_type.id})
        # # print("\n\n\n", data_list[2].get("name"))
