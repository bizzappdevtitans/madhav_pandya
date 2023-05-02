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
        payload = {}
        response = requests.request("GET", url, data=payload)
        data = response.json()
        vals = self.env["project.project"].search(
            [("external_id", "=", self.project_importer)]
        )
        if not vals:
            self.env["project.project"].sudo().create(
                {"external_id": data.get("id"), "name": data.get("name")}
            )

        url_task = (
            "https://api.trello.com/1/boards/%s/cards/?key=d0e8e49052ffc8"
            "d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30294d5058810"
            "e97d"
            "c4b76420ca474c8e9D1B31FC7" % self.project_importer
        )
        payload_task = {}
        reponse_task = requests.request("GET", url_task, data=payload_task)
        data_task = reponse_task.json()
        for tasks_vals in data_task:
            task_values = {
                "name": tasks_vals.get("name"),
                "description": tasks_vals.get("desc"),
                "project_id": vals.id,
            }
            self.env["project.task"].create(task_values)

    def import_task_from_trello(self):
        url_list = (
            "https://api.trello.com/1/boards/rtkZUIhf/lists?key=d0e8e49052f"
            "fc8d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30294d505881"
            "0e97dc4b76420ca474c8e9D1B31FC7"
        )

        payload_list = {}

        response_list = requests.request("GET", url_list, data=payload_list)
        data_list = response_list.json()
        vals = self.env["project.task"].browse(62)
        # print("\n\n\n\n", vals)
        if vals:
            list_type = self.env["project.task.type"].create(
                {"name": data_list[2].get("name")}
            )
        vals.write({"stage_id": list_type.id})
        # print("\n\n\n", data_list[2].get("name"))
