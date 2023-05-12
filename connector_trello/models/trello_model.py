from odoo import fields, models


class TrelloAbstractModel(models.AbstractModel):
    _name = "trello.model"
    _description = "My Abstract Model"

    trello_backend_ids = fields.Many2one(comodel_name="trello.backend")
    external_id = fields.Char("External id")

    # def export_project_changes(self):
    #     # Define your Trello API key and token
    #     api_key = 'd0e8e49052ffc8d9b19945eaff3fec29'
    #     token = 'ATTA9630a7b59094d59905fd4a97a6abff30294d5058810e97dc4b764
    # 20ca474c8e9D1B31FC7'

    #     # Define the URL to create a new board on Trello
    #     board_url = f'https://api.trello.com/1/boards'

    #     # Define the parameters for creating a new board on Trello
    #     board_params = {
    #         'name': self.name,
    #         'key': api_key,
    #         'token': token
    #     }

    #     # Send a POST request to Trello to create a new board
    #     board_response = requests.post(board_url, params=board_params)
    #     board_data = board_response.json()

    #     # Check if the request was successful
    #     if board_response.status_code == 200:
    #         board_id = board_data['id']
    #         board_lists = {}

    #         # Export stages and tasks to the Trello board
    #         for stage in self.type_ids:
    #             print("\n\n\n",stage.external_id)
    #             if stage.name.lower() in ['to do', 'doing', 'done']:
    #                 continue
    #             # Define the URL to create a new list on the board
    #             list_url = f'https://api.trello.com/1/boards/{board_id}/lists'

    #             # Define the parameters for creating a new list on the board
    #             list_params = {
    #                 'name': stage.name,
    #                 'key': api_key,
    #                 'token': token
    #             }
    #             print("\n\n\n\n",stage.name)

    #             # Send a POST request to Trello to create a new list
    #             list_response = requests.post(list_url, params=list_params)
    #             list_data = list_response.json()

    #             # Check if the request was successful
    #             if list_response.status_code == 200:
    #                 list_id = list_data['id']
    #                 board_lists[stage.id] = list_id

    #         for task in self.task_ids:
    #             if task.stage_id.id in board_lists:
    #                 list_id = board_lists[task.stage_id.id]

    #                 # Define the URL to create a new card on the list
    #                 card_url = 'https://api.trello.com/1/cards'

    #                 # Define the parameters for creating a new card on the list
    #                 card_params = {
    #                     'name': task.name,
    #                     'desc': task.description or '',
    #                     'idList': list_id,
    #                     'key': api_key,
    #                     'token': token
    #                 }

    #                 # Send a POST request to Trello to create a new card
    #                 card_response = requests.post(card_url, params=card_params)

    #                 # Check if the request was successful
    #                 if card_response.status_code != 200:
    #                     # Raise an exception if the request was unsuccessful
    #                     card_response.raise_for_status()

    #     else:
    #         # Raise an exception if the request to create the board was unsuccessful
    #         board_response.raise_for_status()
