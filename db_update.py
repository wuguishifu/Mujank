import json

import database

with open('mujank_db.json') as json_file:
    data = json.load(json_file)
    users = data['users']
    for user in list(users):
        user_data = users[user]
        if 'c_id_0002' in user_data['cards']:
            num = user_data['cards']['c_id_0475']
            del user_data['cards']['c_id_0475']
            for i in range(num):
                database.add_card(user, 'c_id_0474')

with open('mujank_db.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
