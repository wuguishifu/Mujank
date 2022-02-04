import json

with open('mujank_db.json') as json_file:
    data = json.load(json_file)
    users = data['users']
    for user in list(users):
        if data['users'][user]['inventory']['coins'] == 30:
            data['users'][user]['inventory']['coins'] -= 30

with open('mujank_db.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
