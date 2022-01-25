import json

with open('mujank_db.json') as json_file:
    data = json.load(json_file)
    users = data['users']
    for user in list(users):
        user_data = users[user]
        if 'inventory' not in user_data:
            user_data['inventory'] = {'items': {}, 'coins': 0}

with open('mujank_db.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
