import xmlrpc.client

import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = "project.project"

    trello_bind_ids = fields.One2many(
        comodel_name="trello.project.project", inverse_name="odoo_id", readonly=True
    )
    external_id = fields.Char("External Id", related="trello_bind_ids.external_id")
    api_key = fields.Char("Api key", related="trello_bind_ids.api_key")
    token = fields.Char("Token Key", related="trello_bind_ids.token")
    project_created_date = fields.Datetime(
        "Created Date", related="trello_bind_ids.project_created_date"
    )
    project_updated_date = fields.Datetime("Updated Date")

    def update_project(self):

        url = "https://api.trello.com/1/boards/%s/?key=%s&token=%s" % (
            self.external_id,
            self.api_key,
            self.token,
        )
        boards = requests.request("GET", url)
        if boards.status_code != 200:
            raise ValidationError(_("Invalid api or token"))
        boards_values = boards.json()
        project = self.env["project.project"].search(
            [("external_id", "=", self.external_id)], limit=1
        )
        if project:
            project.write(
                {
                    "name": boards_values.get("name"),
                    "project_updated_date": fields.Datetime.now(),
                }
            )
        url_list = "https://api.trello.com/1/boards/%s/lists?key=%s&token=%s" % (
            self.external_id,
            self.api_key,
            self.token,
        )
        stage_response = requests.request("GET", url_list)
        if stage_response.status_code != 200:
            raise ValidationError(_("Invalid api or token"))
        stage_data = stage_response.json()

        # Create Odoo stages for each Trello list
        project_stage_obj = self.env["project.task.type"]
        stage_mapping = {}
        for trello_list in stage_data:
            exist_stage = project_stage_obj.search(
                [("external_id", "=", trello_list.get("id"))], limit=1
            )
            if exist_stage:
                stage = exist_stage.write({"name": trello_list.get("name")})
                stage_mapping[trello_list.get("id")] = exist_stage.id
            else:
                stage = project_stage_obj.create(
                    {
                        "name": trello_list.get("name"),
                        "external_id": trello_list.get("id"),
                        "project_external_id": self.external_id,
                    }
                )
                stage_mapping[trello_list.get("id")] = stage.id

        url_task = "https://api.trello.com/1/boards/%s/cards/?key=%s&token=%s" % (
            self.external_id,
            self.api_key,
            self.token,
        )
        reponse_task = requests.request("GET", url_task)
        if reponse_task.status_code != 200:
            raise ValidationError(_("Invalid api or token"))
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
                    "project_external_id": self.external_id,
                }
                self.env["trello.project.task"].create(task_values)

    def view_project_in_trello(self):
        return {
            "type": "ir.actions.act_url",
            "url": f"https://trello.com/b/{self.external_id}/parth-agrawal",
        }

    def export_project_changes(self):
        odoo_base_url = "http://localhost:8088"
        odoo_database = "connector_trello_new"
        odoo_username = "admin"
        odoo_password = "admin"

        # Trello API credentials
        trello_base_url = "https://api.trello.com/1"
        trello_key = self.api_key
        trello_token = self.token
        trello_board_id = self.external_id

        # Connect to Odoo API
        odoo_session = requests.Session()
        odoo_auth_url = f"{odoo_base_url}/web/session/authenticate"
        odoo_auth_payload = {
            "jsonrpc": "2.0",
            "params": {
                "db": odoo_database,
                "login": odoo_username,
                "password": odoo_password,
            },
        }

        odoo_response = odoo_session.post(odoo_auth_url, json=odoo_auth_payload)
        odoo_response.raise_for_status()
        odoo_session_id = odoo_response.json()
        # Extract result
        odoo_session_id.get("result")

        # Extract session_id
        session_id = odoo_session_id.get("result").get("uid")
        # print("\n\n\n\n\n", odoo_session_id["result"]["uid"])
        # pprint.pprint(odoo_session_id)

        # info = xmlrpc.client.ServerProxy("https://demo.odoo.com/start").start()
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(odoo_base_url))
        common.version()
        common.authenticate(odoo_database, odoo_username, odoo_password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(odoo_base_url))
        models.execute_kw(
            odoo_database,
            session_id,
            odoo_password,
            "project.task",
            "search",
            [[("name", "=", True)]],
        )
        # print("\n\n\n\nmodels", models)

        # Retrieve Odoo project data (e.g., tasks)
        odoo_project_url = f"{odoo_base_url}/api/v1/project.task"
        odoo_project_payload = {
            "jsonrpc": "2.0",
            "params": {
                "session_id": session_id,
                "model": "project.task",
                "domain": [],
                "fields": ["name", "description", "status"],
                "limit": 10,
            },
        }
        odoo_response = odoo_session.post(odoo_project_url, json=odoo_project_payload)
        # print("\n\n\n\n", odoo_response)
        if odoo_response.status_code != 200:
            # print(f"Request Error: {odoo_response.content}")
            return
        # odoo_response.raise_for_status()
        odoo_tasks = odoo_response.json()
        # print("\n\n\n\n", odoo_tasks)

        # Connect to Trello API
        trello_session = requests.Session()
        trello_auth_params = {"key": trello_key, "token": trello_token}
        trello_lists_url = f"{trello_base_url}/boards/{trello_board_id}/lists"
        trello_response = trello_session.get(
            trello_lists_url, params=trello_auth_params
        )
        trello_response.raise_for_status()
        trello_lists = trello_response.json()

        # Format and export data to Trello
        for task in odoo_tasks:
            trello_card_url = f"{trello_base_url}/cards"
            trello_card_payload = {
                "key": trello_key,
                "token": trello_token,
                "idList": trello_lists[0][
                    "id"
                ],  # Specify the Trello list ID where the card should be created
                "name": task["name"],
                "desc": task["description"],
                "due": None,  # Optionally set a due date
            }
            trello_response = trello_session.post(
                trello_card_url, params=trello_auth_params, json=trello_card_payload
            )
            trello_response.raise_for_status()
            trello_response.json()
            # print(f"Created Trello card: {trello_card['id']}")

        # # Close the sessions
        # odoo_session.close()
        # trello_session.close()
