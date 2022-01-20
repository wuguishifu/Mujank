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

# unit testing
# database.add_user('bo_lol')

# print(database.get_cards('200454087148437504'))
# print(database.get_num('bo_lol', 'blah blah'))
# print(database.has_card('bo_lol', 'blah blah'))
# database.add_card('bo_lol', 'blah blah')
# database.set_num('bo_lol', 'blah blah', 30)
# database.remove_card('bo_lol', 'blah blah')
# database.delete_card('bo_lol', 'blah blah')

# database.set_claimed('bo_lol', True)
# print(database.check_claimed('bo_lol'))
# database.set_claimed('bo_lol', False)
# print(database.check_claimed('bo_lol'))

# database.dec_rolls('bo_lol')
# database.reset_rolls('bo_lol')
# print(database.get_num_rolls('bo_lol'))

# database.add_user('bo_lol')
# database.add_card('bo_lol', 'bruh')
# database.reset_displayed_card('bo_lol')
# print(database.get_displayed_card('bo_lol'))
# database.remove_card('bo_lol', 'bruh')

# database.reset_all_timers()
# database.add_card_to_wishlist('bo_lol', 'bruh')
# print(database.get_wishlist('bo_lol'))
# database.remove_card_from_wishlist('bo_lol', 'bruh')
# print(database.get_wishlist('bo_lol'))
