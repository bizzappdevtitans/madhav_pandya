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
    task_type_ids = fields.One2many(
        comodel_name="project.task.type", inverse_name="project_id", readonly=True
    )

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
            "url": f"https://trello.com/b/{self.external_id}",
        }

    def export_project_changes(self):
        # Define your Trello API key and token
        api_key = "d0e8e49052ffc8d9b19945eaff3fec29"
        token = "ATTA9630a7b59094d59905fd4a97a6abff30294d5058810e97dc4b76420ca474c8e9D1B31FC7"
        board_lists = {}
        for project in self:
            if project.external_id:
                # Define the URL to update the Trello board
                board_update_url = (
                    "https://api.trello.com/1/boards/%s" % self.external_id
                )

                # Define the parameters for updating the Trello board
                board_params = {"name": project.name, "key": api_key, "token": token}

                # Send a PUT request to Trello to update the board
                board_response = requests.put(board_update_url, params=board_params)
                board_data = board_response.json()
                board_id = board_data["id"]

                # print("\n\n\nBboard Response", board_response)

                # Check if the request was successful
                # if board_response.status_code == 200:
                #     print(f"Board '{project.name}' updated successfully in Trello.")

            else:
                # Define the URL to create a new board on Trello
                board_url = "https://api.trello.com/1/boards"

                # Define the parameters for creating a new board on Trello
                board_params = {"name": project.name, "key": api_key, "token": token}

                # Send a POST request to Trello to create a new board
                board_response = requests.post(board_url, params=board_params)
                board_data = board_response.json()

                # Check if the request was successful
                if board_response.status_code == 200:
                    board_id = board_data["id"]
                    board_lists = {}
                    # Check if the request was successful
                    # if board_response.status_code == 200:
                    #    print("Boarddddd")
                    self.external_id = board_data["id"]
                    # print("New board created successfully.")

        for stage in self.type_ids:
            # print("\n\n\n\n\n",stage)
            # print("Total records:", len(self.type_ids))
            # Check if the stage has an external ID (indicating it exists on Trello)
            if stage.external_id:
                # Define the URL to update the list on Trello
                list_url = (
                    "https://api.trello.com/1/lists/%s?key=d0e8e49052ffc8"
                    "d9b19945eaff3fec29&token=ATTA9630a7b59094d59905fd4a97a6abff30294d5"
                    "058810e97dc4b76420ca474c8e9D1B31FC7"
                )

                # Define the parameters for updating the list on Trello
                list_params = {"name": stage.name, "key": api_key, "token": token}

                # Send a PUT request to Trello to update the list
                list_response = requests.put(list_url, params=list_params)

                list_data = list_response.json()

                # Check if the request was successful
                # if list_response.status_code == 200:
                # List updated successfully
                # print(f'Stage "{stage.name}" updated successfully.')
            else:
                if stage.name.lower() in ["to do", "doing", "done"]:
                    continue
                # Define the URL to create a new list on the board
                list_url = f"https://api.trello.com/1/boards/{board_id}/lists"

                # Define the parameters for creating a new list on the board
                list_params = {"name": stage.name, "key": api_key, "token": token}
                # print("\n\n\n\n", stage.name)

                # Send a POST request to Trello to create a new list
                list_response = requests.post(list_url, params=list_params)
                list_data = list_response.json()

                # Check if the request was successful
                if list_response.status_code == 200:
                    list_id = list_data["id"]
                    board_lists[stage.id] = list_id

        for task in self.task_ids:
            # print("\n\n\n\n\n\n",task)
            # print("Total Taks:", len(self.task_ids))

            if task.external_id:
                # Define the URL to update the card on Trello
                card_update_url = f"https://api.trello.com/1/cards/{task.external_id}"

                # Define the parameters for updating the card on Trello
                card_params = {
                    "name": task.name,
                    "desc": task.description or "",
                    "key": api_key,
                    "token": token,
                }
                # print("\n\n\n", task.name)

                # Send a PUT request to Trello to update the card
                card_response = requests.put(card_update_url, params=card_params)

                # Check if the request was successful
                # if card_response.status_code == 200:
                # Card updated successfully
                # print(f'Task "{task.name}" updated successfully.')
            else:
                if task.stage_id.id in board_lists:
                    list_id = board_lists[task.stage_id.id]

                    # Define the URL to create a new card on the list
                    card_url = "https://api.trello.com/1/cards"

                    # Define the parameters for creating a new card on the list
                    card_params = {
                        "name": task.name,
                        "desc": task.description,
                        "idList": list_id,
                        "key": api_key,
                        "token": token,
                    }

                    # Send a POST request to Trello to create a new card
                    card_response = requests.post(card_url, params=card_params)

                    if card_response.status_code != 200:
                        # Raise an exception if the request was unsuccessful
                        card_response.raise_for_status()
