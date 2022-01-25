import json

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
