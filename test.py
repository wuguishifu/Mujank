import cards
import os
import csv
import json

import database

# with open('mujank_db.json') as json_file:
#     data = json.load(json_file)
#     owned_cards = data['users']['200454087148437504']['cards'].keys()
#     for card_id in owned_cards:
#         print(card_id)
#
# user_data = data['users']
# user_data['bo'] = {'cards': {'c_id_0001': 1, 'c_id_0002': 1, 'c_id_0003': 1}}
# data['users'] = user_data
#
# with open('mujank_db.json', 'w') as json_file:
#     json.dump(data, json_file, indent=4)


with open('mujank_db.json') as json_file:
    data = json.load(json_file)
    users = data['users']
    for user in users:
        if 'cards' not in data['users'][user]:
            data['users'][user]['cards'] = {}
        if 'wishlist' not in data['users'][user]:
            data['users'][user]['wishlist'] = {}


with open('mujank_db.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

